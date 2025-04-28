from urllib.parse import urlparse, urlunparse
from typing import Callable
import sys
import re
import string
import scipy
import pandas as pd
import json

url_total=0
url_count=0
bigram_total = 0
char_total = 0

# Helper functions
# Strip scheme and characters outside _CHAR_SPACE
def strip_url(url: str) -> str:
    url = "".join(char for char in url if char in string.printable[:-6])

    if (scheme := urlparse(url).scheme):
        url = re.sub(f"^{scheme}://", "", url)

    return url 

def char_count(url: str, count: list) -> list:
    url=strip_url(url)
    global char_total
    char_total += len(url)

    global url_count
    url_count+=1
    
    print(f'char_progress:\t{url_count}\t/\t{url_total}\t({url_count/url_total*100:.2f}%)')

    # -6 to remove the whitespace characters
    for i, char in enumerate(string.printable[:-6]):

        count[i] += url.count(char)

    return count

def bigram_count(url: str, count: list) -> list:
    url = strip_url(url)
    global bigram_total
    bigram_total += len(url)-1

    global url_count
    url_count+=1
    
    print(f'bigram_progress:\t{url_count}\t/\t{url_total}\t({url_count/url_total*100:.2f}%)')

    #count = []*len(string.printable)**2
    for i, char in enumerate(url[:-1]):
        idx1 = string.printable.find(char)*len(string.printable[:-6])
        idx2 = string.printable.find(url[i+1]) 
        count[idx1 + idx2] += 1

    return count

 # Calculates the distrubution of each char in the url 
def calc_dist(count: list, total: int) -> list:
    return list(map(lambda x: x/total, count));


def extract_dist():
    
    df = pd.read_csv(sys.argv[1]) 

    global url_total 
    global url_count 
    url_total = len(df.index)

    b_count = [0]*(len(string.printable[:-6])**2)
    c_count = [0]*len(string.printable[:-6])

    df["url"].apply(lambda x: bigram_count(strip_url(x), b_count)) 
    url_count = 0
    df["url"].apply(lambda x: char_count(strip_url(x), c_count)) 


    bigram_dist = calc_dist(b_count, bigram_total)
    char_dist = calc_dist(c_count, char_total)


    with open(sys.argv[2], "w") as out:
        out.write(json.dumps(bigram_dist))
        out.write(json.dumps(char_dist))

extract_dist()    

 
