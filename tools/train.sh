n_runs=3
data=$2

# Setup Possible Layers Configurations
l1="18" # maybe an insane bet
l2="256,128,64,32"
l2="128,64,32"
l3="64,32"
l4="32,16"
layer_cfgs=($l1 $l2 $l3 $l4 $l5)
layer_cfg_cnns=($l2 $l3 $l4)

# Gru and Lstm Hidden State 
hidden_dims=(256 128 64 32 16) # just trial and error

# Kernel Sizes 

kernel_sizes=(6 5 4 3)

# Padding
# padding doesnt appear to  make sense in our case
padding=1

# Out Channels for CNNs

out_channels=(128 64 32)

function run_n_times(){
    local acu
    local averege=0
    for i in {1..3}; do
        acu=$(eval $2 | sed -En 's/\[.*\] Accuracy: (.*)$/\1/p') 
        echo $acu
        averege=$(echo "scale=5; $averege + $acu" | bc)
    done
    
    averege=$(echo "scale=5; $averege / $1" | bc)
    echo $averege
}

# MLP

case $3 in  
	"mlp")
	echo "MLP"
		for layer in ${layer_cfgs[@]}; do
		    options="--model mlp --path $data --options --layers $layer"
		    cmd="pacu train $options"
		    avg=$(run_n_times $n_runs "$cmd") 
		    echo "$options $avg"
		done

	;;
# CNNLSTM
	"cnnlstm")
		echo "CNNLSTM"
		for layer in ${layer_cfg_cnns[@]}; do
		    for out_channel in ${out_channels[@]}; do
			for kernel_size in ${kernel_sizes[@]}; do
			    options="--options --layers $layer --out-channels $out_channel --padding $padding --kernel_size $kernel_size"
			    cmd="pacu train --model cnnlstm --path $data $options"
			    avg=$(run_n_times $n_runs "$cmd")
			    echo "$options $avg"
			done
		    done 
		done
	;;

# CharCNN

	"charcnn")
		echo "CharCNN"
		for layer in ${layer_cfg_cnns[@]}; do
		    for out_channel in ${out_channels[@]}; do
			for kernel_size in ${kernel_sizes[@]}; do
			    options="--options --layers $layer --out-channels $out_channel --padding $padding --kernel_size $kernel_size"
			    cmd="pacu train --model charcnn --path $data $options"
			    avg=$(run_n_times $n_runs "$cmd")
			    echo "$options $avg"
			done
		    done 
		done
	;;
# Siamese 
	"siamese")
		echo "Siamese"
		for layer in ${layer_cfgs[@]}; do
		    options="--model siamese --path $data --options --layers $layer" 
		    cmd="pacu train $options"
		    avg=$(run_n_times $n_runs "$cmd") 
		    echo "$options $avg"
		done
	;;

# GRU
	"gru")
		echo "GRU"
		for hidden_dim in ${hidden_dims[@]}; do
		    options="--model gru --path $data --options --hidden-dim $hidden_dim"
		    cmd="pacu train $options"
		    avg=$(run_n_times $n_runs "$cmd") 
		    echo "$options $avg"
		done
	;;

# LSTM
	"lstm")
		echo "LSTM"
		for hidden_dim in ${hidden_dims[@]}; do
		    options="--model lstm --path $data --options --hidden-dim $hidden_dim"
		    cmd="pacu train $options"
		    avg=$(run_n_times $n_runs "$cmd") 
		    echo "$options $avg"
		done
	;;
esac

# Refs

# gru-hidden-dim: https://discuss.pytorch.org/t/how-to-choose-the-size-of-hidden-size-value/165357
# hidden-layers: https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw    
