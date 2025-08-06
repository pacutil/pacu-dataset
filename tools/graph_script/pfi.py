import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
import numpy as np
import sys


ticks=40
ticks_label=44
axes=40
boxes=36
title=50

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data,vmin=0,vmax=1.2,aspect='equal', **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax,  format="{x:.1f}%", **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="baseline", labelpad=60, fontsize=ticks_label, weight='extra bold')
    cbar.set_ticks(np.arange(0,1.21,0.2))
    cbar.ax.tick_params( labelsize=ticks)

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels, rotation=-30, ha="right", rotation_mode="anchor", fontsize=axes, style='italic')
    ax.set_yticks(range(data.shape[0]), labels=row_labels,fontsize=axes)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i,  valfmt(data[i, j], None),fontsize=boxes,**kw)
            texts.append(text)

    return texts


df = pd.read_csv(f'{sys.argv[1]}')
models = df["model"] 
baseline = df["baseline"]
df = df.drop(columns=["model","baseline"])


#df = df.drop(columns= ["has_ip","number_count","dash_symbol_count","url_length","url_depth","subdomain_count","query_params_count","has_port"])



df1 = pd.DataFrame(df, columns=["has_ip","number_count","dash_symbol_count","url_length","url_depth","subdomain_count","query_params_count","has_port"])

df = df1

for c in df.columns:
    df[c] = -1 * (df[c] - baseline) / baseline * 100


fig, ax = plt.subplots(figsize=(35,15))

data = df.to_numpy()

im,cbar = heatmap(data, models.values, df.columns.values, ax=ax, cmap="YlOrRd", cbarlabel="Perda Relativa de Acurácia")

texts =  annotate_heatmap(im, valfmt="{x:.2f}%")



plt.title("Permutação de Features", fontsize=title, weight='extra bold', pad=40)

#ax.pcolormesh(data)


plt.savefig("pfi",  bbox_inches='tight', pad_inches=0.5, dpi=300)
#plt.show()
