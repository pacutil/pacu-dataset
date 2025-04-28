#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>    
#include <sys/mman.h>
#include <sys/stat.h>
#include <string.h>
#include <unistd.h>  
#include <stdatomic.h>
#include <semaphore.h>
#include <pthread.h>

#include "line_count.h"
#define MAX_FILE 23 
#define SAMPLE_SIZE 2200000

static sem_t s;
static sem_t a;

static int fname = 1;

FILE* ffopen (const char* pathname, const char* mode, int index){
    char fmt_filename[64] = {0};
    sprintf(fmt_filename, pathname, index); 
    return fopen(fmt_filename, mode);        
}


char* load_file(FILE* file, size_t* size) {
    struct stat stats; // holds file stats 
    char* map;
    int error;

    error = fstat(fileno(file), &stats);
    if (error == -1){
        *size = 0;
        return NULL; 
    }
    *size = stats.st_size;

    map = mmap(NULL, *size, PROT_READ, MAP_PRIVATE|MAP_POPULATE , fileno(file), 0);
    if(map == MAP_FAILED){
	fprintf(stderr, "mmap was the culprit\n");
        return NULL;
    }
    
    error = madvise(map, *size, MADV_WILLNEED | MADV_HUGEPAGE);
    if (error == -1){
	fprintf(stderr, "madvise was the culprit\n");
        return NULL;
    }

    /*
    error = mlock(map, *size);
    if (error == -1){
	fprintf(stderr, "mlock was the culprit\n");
        return NULL;
    }*/
    return map;
}

void drop_file(char* map, size_t size){
    munlock(map,size);
    munmap(map, size);

    return;
}

int cmp(const void* a, const void* b){
    return *(int*)a - *(int*)b;
}

unsigned long* generate_ordered_sample_idx(unsigned long size, unsigned long range){
    srandom(time(NULL)*range); 
    
    unsigned long* smp_lines = malloc(size*sizeof*smp_lines);

    for (unsigned long i = 0; i < size; i++)
        smp_lines[i] = random()%(range-1); // -1 because i dont want to deal with an EOF 
    
    qsort(smp_lines, size, sizeof*smp_lines, cmp); 

    return smp_lines;
}

void sampling(FILE* dest, FILE* src, unsigned long sample_size, int file_id) {
    size_t src_size;
    char *src_map, *line;
    unsigned long src_lines, *smp_idx, idx = 0, smp_count = 0;

    // Maps the file into memory, hints the kernel
    // to preload the pages and make the pages
    // permanent in memory
    sem_wait(&s);
    src_map = load_file(src, &src_size);
    if (!src_map){
	fprintf(stderr, "couldnt map file\n");
	exit(1);
    }	
    sem_post(&s);

    // Generate the random index 
    src_lines = line_counts[file_id - 1];
    smp_idx = generate_ordered_sample_idx(sample_size, src_lines); 

    line = src_map;
    while (idx <= src_size && smp_count < sample_size){
	
       // Checks the rest of the file for \n
       char* endline = memchr(line, '\n', (src_map+src_size) -line); 
       if(!endline){        
            // Shouldnt happen, but who knows
            drop_file(src_map, src_size);
            free(smp_idx);
            return;
       }
       
       if (idx == smp_idx[smp_count]){   
           fprintf(dest, "%.*s\n", (int)(endline - line), line);
		   printf("fname %d\t%ld\t/%ld\t(%.2f%%)\n", fname, smp_count, sample_size, ((float)smp_count)/sample_size*100);  	   
		   do {
		   		smp_count++;
		   } while( smp_idx[smp_count] == smp_idx[smp_count-1] && smp_count < sample_size);
       }

       line = endline + 1; 
       idx++;
    } 

    drop_file(src_map, src_size);
    free(smp_idx);
    return;
}

static void* run(void* asd) {
    FILE *sample, *source;
    int file;

    sem_wait(&a);

    if (fname > MAX_FILE) {
        return NULL;
    }
        
    source = ffopen("%d", "r", fname);
    if (!source) {
	    exit(1);
    }

    sample = ffopen("sample%d", "w", fname);
    if (!source) {
	    exit(1);
    }

	file = fname++;

    sem_post(&a);
    
    sampling(sample, source, SAMPLE_SIZE, file);

    fclose(sample);
    fclose(source);

    return NULL;
}

int main(){
    int ret = sem_init(&s, 0, 1);
    if (ret) {
        fprintf(stderr, "Initialization failed\n");
        exit(1);
    }

    ret = sem_init(&a, 0, 1);
    if (ret) {
        fprintf(stderr, "Initialization failed\n");
        exit(1);
    }

    for (; fname <= MAX_FILE;) {
        pthread_t thread1, thread2;
        int iret1, iret2;
        iret1 = pthread_create(&thread1, NULL, run, NULL);
        if (iret1) {
            fprintf(stderr, "Initialization failed\n");
            exit(1);
        }

        iret2 = pthread_create(&thread2, NULL, run, NULL);
        if (iret2) {
            fprintf(stderr, "Initialization failed\n");
            exit(1);
        }
        pthread_join(thread1, NULL);
        pthread_join(thread2, NULL);
			
    }
	
    return 0;
}
