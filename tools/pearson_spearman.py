import pandas as pd
import numpy as np
import sys
from sklearn.feature_selection import r_regression
from scipy.stats import spearmanr
from itertools import combinations


df = pd.read_csv(sys.argv[1])
fi = pd.DataFrame()

if "url" in df.columns:
    df = df.drop(columns=["url"])

labels = df["label"]

#df = df.drop(columns=["label","has_ip","number_count","dash_symbol_count", "url_length", "url_depth","subdomain_count","query_params_count","has_port"])
df = df.drop(columns=["label"])


max_kl_big = df[(df['kl_big'] != np.inf) & (df['kl_big'] != -np.inf)]['kl_big'].max()
max_kl_char = df[(df['kl_char'] != np.inf) & (df['kl_char'] != -np.inf)]['kl_char'].max()
min_kl_big = df[(df['kl_big'] != np.inf) & (df['kl_big'] != -np.inf)]['kl_big'].min()
min_kl_char = df[(df['kl_char'] != np.inf) & (df['kl_char'] != -np.inf)]['kl_char'].min()

df["kl_big"] = df["kl_big"].replace(np.inf, min(2*max_kl_big, sys.float_info.max))
df["kl_char"] = df["kl_char"].replace(np.inf, min(2*max_kl_char, sys.float_info.max))
df["kl_big"] = df["kl_big"].replace(np.inf, max(2*min_kl_big, sys.float_info.min))
df["kl_char"] = df["kl_char"].replace(np.inf, max(2*min_kl_char, sys.float_info.min))


def k_feature_importance(df, k):
    combs = list(combinations(df.columns, k))
    for combination in combs:
        combination = list(combination)
        print(spearmanr(df[combination].values,labels.values))
        


for feature in df.columns:

    f = df[feature].values.reshape(-1,1)
    l = labels.values

    r = r_regression(f, l)
    s = spearmanr(f, l)
    fi[feature] = [r[0], s[0],s[1]] 


fi.to_csv(sys.argv[2], index=False)




