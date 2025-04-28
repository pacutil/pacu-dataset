#!/bin/bash

batch_size=16

while [ 1 ]; do
    echo "Attempt Batch Size: $batch_size"
    cmd="pacu train --model mlp --path $1 --batch-size $batch_size --epochs 1"
    eval $cmd

    if [[ $? -eq 0 ]]; then 
        echo "Successeful Batch Size: $batch_size"
    else 
        echo "Failed Batch Size: $batch_size"
    fi

    batch_size=$(($batch_size*2))
done

