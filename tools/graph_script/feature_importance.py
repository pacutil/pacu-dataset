import sys
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1])

print(df.columns.values)

print(df.iloc[1].values)

plt.bar(df.columns.values,df.iloc[1].values)

plt.show()
