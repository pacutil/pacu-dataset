import os
import sys

features = ["has_ip", "number_count", "dash_symbol_count", "url_length", "url_depth", "subdomain_count", "query_params_count", "has_port", "ks_char", "kl_char", "eucli_char", "cs_char", "man_char", "ks_big", "kl_big", "eucli_big", "cs_big", "man_big", "huffman"]


pacu = f'pacu train --rf --path {sys.argv[1]}'

file = f'>> {sys.argv[2]'

# baseline
os.system('echo baseline' + file)
os.system(pacu + file)

for feature in features:
    os.system(f'echo {feature}' + file)
    cmd = pacu + f'--random {feature}' + file
    os.system(cmd) 
