import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def mysavefig(fig,fileName='plot',fileType='pdf', dpi=300,folder=None):
    if folder is None:
        folder = '~/Desktop/'
    fullfile = '%s%s.%s'%(folder,fileName,fileType)
    fig.savefig(fullfile, bbox_inches = 'tight', transparent=True)

def sigdiffs_initialize():
    sigdiffs = pd.DataFrame(columns=['leftBar','rightBar','pval'])
    return sigdiffs

def add_relationship(sigdiffs,relationship = [0,1,0.001]):
    sigdiffs = sigdiffs.append(pd.DataFrame([relationship],columns=sigdiffs.columns))
    sigdiffs = sigdiffs.reset_index(drop=True)
    return sigdiffs

def add_relationships(sigdiffs = None,relationships = [[0,1,0.001]]):
    if sigdiffs == None:
        sigdiffs = sigdiffs_initialize()
    for i, relationship in enumerate(relationships):
        sigdiffs = add_relationship(sigdiffs,relationship)
    sigdiffs = sigdiffs.reset_index(drop=True)
    return sigdiffs

def add_stars(sigdiffs):
    for i in sigdiffs.index:
        if sigdiffs.loc[i,'pval'] <= 0.001:
            sigdiffs.loc[i,'stars'] = '***'
        elif sigdiffs.loc[i,'pval'] <= 0.01:
            sigdiffs.loc[i,'stars'] = '**'
        elif sigdiffs.loc[i,'pval'] <= 0.05:
            sigdiffs.loc[i,'stars'] = '*'
        else:
            sigdiffs.loc[i,'stars'] = 'n.s.'
        sigdiffs.loc[i,'pval_str'] = 'p = %.3f'%sigdiffs.loc[i,'pval']#str(sigdiffs.loc[i,'pval'])
    return sigdiffs

def add_sig_markers(ax,relationships=[[0,1,0.001]],linewidth=1,caps=True,
	interact_caps=False, interact_caps_width = None, ystart = None,distScale=1, markerType = 'symbol'):
    ylim_start = ax.get_ylim()
    sigdiffs = add_relationships(relationships = relationships)
    sigdiffs = add_stars(sigdiffs)
    fontHeightInch = sns.plotting_context()['font.size']/72
    axHeightInch = ax.get_figure().get_size_inches()[1]
    numMarkers = sigdiffs.shape[0]
    markersHeightInch = numMarkers*3*distScale*fontHeightInch
    markerFraction = markersHeightInch/axHeightInch # The fraction of the figure that will be sig markers
    figureFraction = 1 - markerFraction
    ylim_end = [ylim_start[0], ylim_start[1]*(1/figureFraction)]
    ax.set_ylim(ylim_end)
    if caps:
        markerHeight = markerFraction*ylim_end[1]/(3*numMarkers)
    else:
        markerHeight = 0
    col = 'k'
    if ystart == None:
        y = ylim_start[1]
    else:
        y = ystart
        ax.set_ylim([ylim_end[0],ylim_end[1]-(ylim_start[1]-ystart)]) # Correct ylim for the shift made by ystart 
    for i in sigdiffs.index:
        x1, x2 = sigdiffs.loc[i,['leftBar','rightBar']]
        ax.plot([x1, x1, x2, x2], [y, y+markerHeight, y+markerHeight, y], lw=linewidth, c=col)
        if interact_caps:
        	if interact_caps_width is not None:
        		ax.plot([x1-interact_caps_width,x1+interact_caps_width],[y,y], lw=linewidth, c=col)
        		ax.plot([x2-interact_caps_width,x2+interact_caps_width],[y,y], lw=linewidth, c=col)
            	# ax.plot([x1-markerHeight,x1+markerHeight],[y,y], lw=linewidth, c=col)
            	# ax.plot([x2-markerHeight,x2+markerHeight],[y,y], lw=linewidth, c=col)
        if markerType == 'symbol':
            ax.text((x1+x2)*.5, y+markerHeight, sigdiffs.loc[i,'stars'], ha='center', va='bottom', color=col)
        elif markerType == 'pval':
            ax.text((x1+x2)*.5, y+markerHeight, sigdiffs.loc[i,'pval_str'], ha='center', va='bottom', color=col)
        y = y + 3*markerHeight
    ax.set_ylim([ax.get_ylim()[0],np.maximum(ax.get_ylim()[1]+markerHeight,ylim_start[1])])

def add_subplot_letter(ax,letter='A',fontsize=24,fontweight='bold',x_shift = 0):
    if len(ax.get_yticklabels()) > 0: # If y axis has tick labels => move more left
        x_shift -= .1
    ax.text(-.1+x_shift,1.1,letter,transform=ax.transAxes,fontsize=fontsize,fontweight=fontweight)

def mydesign(style='grey',palette='tab10',context='talk'):
    if style == 'grey':
        sns.set_style('darkgrid', {"axes.facecolor": ".95"})
    sns.set_palette(palette)
    sns.set_context(context)

