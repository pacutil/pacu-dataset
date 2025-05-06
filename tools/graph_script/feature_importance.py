import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data

df = pd.read_csv(sys.argv[1])
columns  = df.loc[0].sort_values(ascending=False).index
df = df[columns]


# Plot

fig, ax = plt.subplots(figsize=(18,7))

bar_width = 0.4 

label_locations = np.arange(len(df.columns.values))


ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

ax.bar(label_locations, df.iloc[1].values, width=bar_width, edgecolor='black' , linewidth=2, orientation='vertical', label="Spearman")
ax.bar(label_locations+bar_width, df.iloc[0].values, width=bar_width, edgecolor='black' , linewidth=2, orientation='vertical',label="Pearson")

ax.set_xticks(label_locations+bar_width, df.columns.values)


# Ticks

plt.xticks(fontsize=16,rotation=90, style='italic')
plt.yticks(ticks=np.arange(-1,1.1,0.2),fontsize=16)

# Labels

plt.title("Correlação de Pearson e Spearman entre Features e Labels", fontsize=20, weight='extra bold')
plt.xlabel("Features", fontsize=18, weight='extra bold')

plt.legend(loc='upper right', ncols=2, fontsize=12, alignment='center')

# Grid 

ax.grid(axis='y', ls='--')
ax.set_axisbelow(True)

# Savefig

plt.savefig("pearson-feature-relation", edgecolor='black',bbox_inches='tight', pad_inches=0.5, dpi=300)

