#!/bin/bash

maxsize=24
cfile=1

for file in cc*; do
    if [[ $(du -k -BG $cfile | cut -dG -f1 ) -ge $maxsize ]]; then 
        cfile=$((cfile+1))
        echo "New File: $cfile"
    fi

    if [[ ! -e $cfile ]]; then
        echo "Creating new file $cfile"
        touch $cfile
    fi

    echo "File $cfile: `du -k -BG $cfile | cut -f1`"
    echo "Appending file $file ..."
    cat $file >> $cfile
    echo "Remove $file"
    rm $file
done
