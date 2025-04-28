#!/bin/bash 


if [[ ! $# -eq 3 ]]; then
    echo "usage $0 <start-year> <end-year>"
    echo "Obs: data available from 2020 to 2025"
    exit 1
fi

# receives a file name like 2017-22, then downloads all the links and takes select the portuguese ones
download-data () {
    for i in $(seq -w 0 299); do
        echo "$1 - $i/299"
        curl "https://data.commoncrawl.org/cc-index/collections/CC-MAIN-$1/indexes/cdx-00$i.gz" > data/cc-$1-00$i.gz
        echo "Descomprimindo"
        gzip -dcv data/cc-$1-00$i.gz > data/temp-$1-00$i
        
        echo "Filtrando urls"
        cat data/temp-$1-00$i | grep '".*por.*"' | sed -E 's/.*"url": "(.*)", "mime".*/\1/' > data/cc-$1-00$i
        rm data/cc-$1-00$i.gz
        rm data/temp-$1-00$i 
    done  
}

mkdir data 2> /dev/null
for i in $(seq $1 $2); do
    cat cc-index| while read file; do 
        download-data $file
    done
done



