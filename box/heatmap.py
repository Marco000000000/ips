import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib import cm
from scipy.interpolate import griddata


def magnmap(data, token, inter, colormap):
    print(token)

    df = pd.DataFrame(data, columns=['TimeStamp', 'idp', 'X', 'Y', 'mx', 'my', 'mz', 'Z', 'lat', 'long'])
    x, y, vals = df['X'].values, df['Y'].values, df['Z'].values

    levels = np.linspace(vals.min(), vals.max(), 6)

    print(x, y, vals)
    print(type(x))

    minx = int(np.min(x))
    maxx = int(np.max(x))
    miny = int(np.min(y))
    maxy = int(np.max(y))

    X, Y = np.meshgrid(np.linspace(minx, maxx, maxx - minx), np.linspace(miny, maxy, maxy - miny))

    interpolated_vals = griddata((x, y), vals, (X, Y), method=inter)

    qim = Image.open(os.getcwd() + "/static/data/" + token + "/origin.png")
    w, h = qim.size
    fim = os.getcwd() + "/static/data/" + token + "/origin.png"
    im = plt.imread(fim)
    fig, ax = plt.subplots()
    im = ax.imshow(im, extent=[0, int(w), int(h), 0])
    ccm = cm.jet
    if colormap == "jet":
        ccm = cm.jet
    elif colormap == "ocean":
        ccm = cm.ocean
    elif colormap == "gnuplot":
        ccm = cm.gnuplot

    cs = ax.contourf(X, Y, interpolated_vals, levels=levels, cmap=ccm, alpha=.8)

    fig.colorbar(cs, ax=ax, shrink=0.9)

    # plt.show()
    namefig = os.getcwd() + "/static/data/" + token + "/hm.png"
    plt.savefig(namefig, dpi=800)

    # x = np.linspace(-1,1,100)
    # y =  np.linspace(-1,1,100)
    # X, Y = np.meshgrid(x,y)

    return namefig
