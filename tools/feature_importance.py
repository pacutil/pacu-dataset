import pandas as pd
import sys


df = pd.read_to_csv(sys.argv[1])

df.drop(columns=["url","has_ip","number_count","dash_symbol_count", "url_length", "url_depth","subdomain_count","query_params_count","has_port"])

df
