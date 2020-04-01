import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import umap
import fcsparser
import os, os.path
import matplotlib.patches as mpatches
plt.style.use('seaborn')

def SimpleOverlay(filebig, filesmall, title, label1, label2, savespace):
    dfbig = []
    for files in os.listdir(filebig):
        pathname = os.path.join(filebig, files)
        if '.DS_Store' not in pathname:
            if os.path.isfile(pathname):
                dfbig.append(fcsparser.parse(pathname)[1])
    dfbigcomb = pd.concat(dfbig)

    titles = list(dfbigcomb.columns)
    channels = titles[4:len(titles)-2]

    dfbigadj = dfbigcomb[channels].applymap(lambda x:np.arcsinh(x/150))
    dfbigadj['FSC-A'] = dfbigcomb['FSC-A']/dfbigcomb['FSC-A'].max() * 10
    dfbigadj['SSC-A'] = dfbigcomb['SSC-A']/dfbigcomb['FSC-A'].max() * 10
    
    dfsmall = []
    for files in os.listdir(filesmall):
        pathname = os.path.join(filesmall, files)
        if '.DS_Store' not in pathname:
            if os.path.isfile(pathname):
                dfsmall.append(fcsparser.parse(pathname)[1])
    dfsmallcomb = pd.concat(dfsmall)
    
    ###Used to use this, but realized that I never use dfsmalladj
    #dfsmalladj = dfsmallcomb[channels].applymap(lambda x:np.arcsinh(x/150))
    #dfsmalladj['FSC-A'] = dfsmallcomb['FSC-A']/dfsmallcomb['FSC-A'].max() * 10
    #dfsmalladj['SSC-A'] = dfsmallcomb['SSC-A']/dfsmallcomb['FSC-A'].max() * 10

    ctime = dfbigcomb['Time'].isin(dfsmallcomb['Time'])
    rowtime = np.where(ctime == True)[0]
    rowind = list(rowtime)
    notrowtime = np.where(ctime == False)[0]
    notrowind = list(notrowtime)

    e = umap.UMAP(random_state=0).fit_transform(dfbigadj)

    plt.scatter(e[rowind,0], e[rowind,1], s=.1, c='r')
    plt.scatter(e[notrowind,0], e[notrowind,1], s=.1, c=('#ABB2B9'))
    plt.title(title)
    plt.xticks([])
    plt.yticks([])
    redp = mpatches.Patch(color='red', label=label1)
    greyp = mpatches.Patch(color=('#ABB2B9'), label=label2)
    plt.legend(handles=[redp, greyp])
    plt.savefig(savespace, dpi=300)


SimpleOverlay('/Users/william/Documents/Botchwey Lab/UMAP/UMAP_FCS/Lauren VPC Paper UMAPs Overlay/WT CD11b+', '/Users/william/Documents/Botchwey Lab/UMAP/UMAP_FCS/Lauren VPC Paper UMAPs Overlay/WT Neuts', 'Wild Type CD11b+ Overlayed with Neutrophils', 'Neutrophils', 'CD11b+', '/Users/william/Documents/Botchwey Lab/UMAP/UMAP Pics/Lauren VPC Paper Overlay 11:22:19/WTCD11b:WTN.png')

