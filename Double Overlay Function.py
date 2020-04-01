import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import umap
import fcsparser
import os, os.path
import matplotlib.patches as mpatches
plt.style.use('seaborn')

def SimpleOverlay(filebig, bluefolder, redfolder, title, bluelabel, redlabel, nonelabel, savespace):
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
    
    dfblue = []
    for files in os.listdir(bluefolder):
        pathname = os.path.join(bluefolder, files)
        if '.DS_Store' not in pathname:
            if os.path.isfile(pathname):
                dfblue.append(fcsparser.parse(pathname)[1])
    dfbluecomb = pd.concat(dfblue)
    
    dfred = []
    for files in os.listdir(redfolder):
        pathname = os.path.join(redfolder, files)
        if '.DS_Store' not in pathname:
            if os.path.isfile(pathname):
                dfred.append(fcsparser.parse(pathname)[1])
    dfredcomb = pd.concat(dfred)
    

    cbtime = dfbigcomb['Time'].isin(dfbluecomb['Time'])
    browtime = np.where(cbtime == True)[0]
    browind = list(browtime)
    bnotrowtime = np.where(cbtime == False)[0]
    bnotrowind = list(bnotrowtime)
    
    crtime = dfbigcomb['Time'].isin(dfredcomb['Time'])
    rrowtime = np.where(crtime == True)[0]
    rrowind = list(rrowtime)
    rnotrowtime = np.where(crtime == False)[0]
    rnotrowind = list(rnotrowtime)

    e = umap.UMAP(random_state=0).fit_transform(dfbigadj)

    plt.scatter(e[bnotrowind,0], e[bnotrowind,1], s=.1, c=('#ABB2B9'))
    plt.scatter(e[rnotrowind,0], e[rnotrowind,1], s=.1, c=('#ABB2B9'))
    plt.scatter(e[rrowind,0], e[rrowind,1], s=.1, c='r')
    plt.scatter(e[browind,0], e[browind,1], s=.1, c='b')
    plt.title(title)
    plt.xticks([])
    plt.yticks([])
    redp = mpatches.Patch(color='red', label=redlabel)
    bluep = mpatches.Patch(color='b', label=bluelabel)
    greyp = mpatches.Patch(color=('#ABB2B9'), label=nonelabel)
    plt.legend(handles=[redp, bluep, greyp])
    #plt.savefig(savespace, dpi=300)

 
