import polars as pl
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations, product
import matplotlib.patches as mpatches


from BigEDA.preprocessing import columns_names

######################################################################################################################

def get_ticks(min, max, n_ticks, n_round=2):
    step = (max - min) / (n_ticks - 1)
    ticks = np.arange(min, max, step)
    if ticks[-1] != max:
       ticks = np.append(ticks, max)
    ticks = np.round(ticks, n_round)
    return ticks

######################################################################################################################

def get_frequencies(X):
    unique_values, counts = np.unique(X, return_counts=True)
    rel_freq = counts/len(X)
    return unique_values, rel_freq

######################################################################################################################

def histogram(X, bins, color, figsize=(9,5), n_xticks=15, x_rotation=0, get_intervals=False, 
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid', n_round_xticks=2) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        
        X = X.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the histogram.
    p = sns.histplot(x=X, stat="proportion", bins=bins, color=color)

    # Setting the sticks for the histogram.
    min = np.floor(X.min())
    max = np.ceil(X.max())
    xticks = get_ticks(min, max, n_ticks=n_xticks, n_round=n_round_xticks)
    plt.xticks(xticks, rotation=x_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'Histogram'+' - '+ X.name, fontsize=15)

    if get_intervals == True :

        interval = dict()
        for i, bar in enumerate(p.patches) :
            interval[i] = f'({bar.get_x()}, {bar.get_x() + bar.get_width()})'
        return interval
    
    if save == True :

        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

######################################################################################################################

def histogram_matrix(df, bins, n_cols, title, figsize=(15,15), auto_col=False, 
                     quant_col_names=[], remove_columns=[], add_columns=[], 
                     n_xticks=15, title_fontsize=15, subtitles_fontsize=11, save=False, 
                     file_name=None, random=False, n=None, fraction=None, seed=123, 
                     x_rotation=0, y_rotation=0, title_height=0.95, style='whitegrid', hspace=1, wspace=0.2,
                     n_round_xticks=2, title_weight='bold', xlabel_size=11, ylabel_size=11, 
                     xticks_size=10, yticks_size=10) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Selecting automatically the quantitative columns.
    if auto_col == True :
        quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])

        if len(remove_columns) > 0 :
            for r in remove_columns :
                quant_col_names.remove(r)

        if len(add_columns) > 0 : 
            for r in add_columns :
                quant_col_names.append(r)

    # Selecting automatically the quantitative columns.
    elif auto_col == False :
        quant_col_names = quant_col_names
   
    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(quant_col_names) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(quant_col_names))

    # Defining a ecdf-plot for each variable considered.
    for (i, col), color in zip(enumerate(quant_col_names), colors) :
      
        ax = axes[i]  # Get the current axis
        X = df.select(col).to_numpy().flatten()
        sns.histplot(data=X, stat="proportion", bins=bins, color=color, ax=ax)
        ax.set_title(col, fontsize=subtitles_fontsize)
        min = np.floor(df[col].min())
        max = np.ceil(df[col].max())
        xticks = get_ticks(min, max, n_ticks=n_xticks, n_round=n_round_xticks)
        ax.set_xticks(xticks)
        ax.tick_params(axis='x', rotation=x_rotation, labelsize=xticks_size)
        ax.tick_params(axis='y', rotation=y_rotation, labelsize=yticks_size)
        ax.set_xlabel(col, size=xlabel_size)
        ax.set_ylabel('Proportion', size=ylabel_size)

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(quant_col_names), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height, weight=title_weight)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

######################################################################################################################
    
def boxplot(X, color, figsize=(9,5), n_xticks=15, x_rotation=0, statistics=None, 
            random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
            style='whitegrid', lines_width=0.55, bbox_to_anchor=(0.5,-0.5), legend_size=10,
              color_stats=None) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :   
        X = X.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the histogram.
    p = sns.boxplot(x=X, color=color)

    # Setting the sticks for the histogram.
    min = np.floor(X.min())
    max = np.ceil(X.max())
    xticks_index = np.unique(np.round(np.linspace(min, max, n_xticks)))
    plt.xticks(xticks_index, rotation=x_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'Boxplot'+' - '+ X.name, fontsize=15)

    if statistics is not None :

        n_statistics = len(statistics)
        if color_stats is None:
            color_stats = sns.color_palette("tab10", n_statistics)
        color_dict = {stat : color for color, stat in zip(color_stats, statistics)}

        if 'median' in statistics :
            median = X.median()
            plt.vlines(x=median, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['median'], linestyles='dashed', label='median', zorder=4)

        if 'mean' in statistics :
            mean = X.mean()
            plt.vlines(x=mean, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['mean'], linestyles='dashed', label='mean', zorder=4)

        if 'Q25' in statistics :
            Q25 = X.quantile(0.25)
            plt.vlines(x=Q25, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['Q25'], linestyles='dashed', label=f'Q25', zorder=4)

        if 'Q75' in statistics :
            Q75 = X.quantile(0.75)
            plt.vlines(x=Q75, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['Q75'], linestyles='dashed', label=f'Q75', zorder=4)

        handles, _ = p.get_legend_handles_labels()
        plt.legend(handles=handles, labels=statistics,  loc='lower center', bbox_to_anchor=bbox_to_anchor, 
                      ncol=n_statistics, fontsize=legend_size)

    if save == True :

        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

######################################################################################################################
    
def boxplot_matrix(df, n_cols, title, figsize=(15,15), auto_col=False, 
                    quant_col_names=[], remove_columns=[], add_columns=[], 
                    n_xticks=10, title_fontsize=15, subtitles_fontsize=12, save=False, file_name=None, 
                    random=False, n=None, fraction=None, seed=123, x_rotation=0, title_height=0.95,
                    style='whitegrid', hspace=1, wspace=0.2, statistics=None, lines_width=0.55, 
                    bbox_to_anchor=(0.5,-0.5), legend_size=10, color_stats=None, n_round_xticks=2, title_weight='bold',
                    xlabel_size=11, xticks_size=10) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Selecting automatically the quantitative columns.
    if auto_col == True :
        quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])

        if len(remove_columns) > 0 :
            for r in remove_columns :
                quant_col_names.remove(r)

        if len(add_columns) > 0 : 
            for r in add_columns :
                quant_col_names.append(r)

    # Selecting automatically the quantitative columns.
    elif auto_col == False :
        quant_col_names = quant_col_names
   
    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(quant_col_names) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(quant_col_names))

    # Defining a ecdf-plot for each variable considered.
    for (i, col), color in zip(enumerate(quant_col_names), colors) :
      
        ax = axes[i]  # Get the current axis
        X = df.select(col).to_numpy().flatten()
        sns.boxplot(x=X, color=color, ax=ax)
        ax.set_title(col, fontsize=subtitles_fontsize)
        min = df[col].min()
        max = df[col].max()
        xticks = get_ticks(min, max, n_ticks=n_xticks, n_round=n_round_xticks)
        ax.set_xticks(xticks)
        ax.tick_params(axis='x', rotation=x_rotation, labelsize=xticks_size)
        ax.set_xlabel(col, size=xlabel_size)
        ax.set_ylabel('')

        if statistics is not None :

           n_statistics = len(statistics)
           if color_stats is None:
               color_stats = sns.color_palette("tab10", n_statistics)
           color_dict = {stat : color for color, stat in zip(color_stats, statistics)}

           if 'median' in statistics :
               median = np.median(X)
               ax.vlines(x=median, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['median'], 
                          linestyles='dashed', label='median', zorder=4)

           if 'mean' in statistics :
               mean = np.mean(X)
               ax.vlines(x=mean, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['mean'], 
                          linestyles='dashed', label='mean', zorder=4)

           if 'Q25' in statistics :
               Q25 = np.quantile(X, 0.25)
               ax.vlines(x=Q25, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['Q25'], 
                          linestyles='dashed', label=f'Q25', zorder=4)

           if 'Q75' in statistics :
               Q75 = np.quantile(X, 0.75)
               ax.vlines(x=Q75, ymin=-0.1 - lines_width/2, ymax=0.1 + lines_width/2, colors=color_dict['Q75'], 
                          linestyles='dashed', label=f'Q75', zorder=4)

           handles, _ = ax.get_legend_handles_labels() 
           fig.legend(handles, statistics, loc='lower center', 
                       bbox_to_anchor=bbox_to_anchor, ncol=len(statistics), fontsize=legend_size)

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(quant_col_names), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height, weight=title_weight)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()

######################################################################################################################

def ecdfplot(X, color, figsize=(9,5), n_xticks=15, n_yticks=10, x_rotation=0, y_rotation=0, complementary=False, 
            random=False, n=None, fraction=None, seed=123, save=False, file_name=None, n_round_xticks=2) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    if random == True :
        
        X = X.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the histogram.
    p = sns.ecdfplot(x=X, color=color, complementary=complementary)

    # Setting the sticks for the histogram.
    min = np.floor(X.min())
    max = np.ceil(X.max())
    xticks = get_ticks(min, max, n_ticks=n_xticks, n_round=n_round_xticks)
    yticks = np.unique(np.round(np.linspace(0, 1, n_yticks), 2))
    plt.xticks(xticks, rotation=x_rotation) 
    plt.yticks(yticks, rotation=y_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'ECDFplot'+' - '+ X.name, fontsize=15)

    if save == True :

        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

######################################################################################################################

def ecdfplot_matrix(df, n_cols, title, complementary=False, figsize=(15,15), auto_col=False, 
                     quant_col_names=[], remove_columns=[], add_columns=[], 
                     n_xticks=15, title_fontsize=15, subtitles_fontsize=11, save=False, file_name=None, 
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, title_height=0.95,
                     style='whitegrid', hspace=1, wspace=0.2, n_round_xticks=2) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Selecting automatically the quantitative columns.
    if auto_col == True :
        quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])

        if len(remove_columns) > 0 :
            for r in remove_columns :
                quant_col_names.remove(r)

        if len(add_columns) > 0 : 
            for r in add_columns :
                quant_col_names.append(r)

    # Selecting automatically the quantitative columns.
    elif auto_col == False :
        quant_col_names = quant_col_names
   
    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(quant_col_names) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(quant_col_names))

    # Defining a ecdf-plot for each variable considered.
    for (i, col), color in zip(enumerate(quant_col_names), colors) :
      
        ax = axes[i]  # Get the current axis
        X = df.select(col).to_numpy().flatten()
        sns.ecdfplot(x=X, color=color, complementary=complementary, ax=ax)
        ax.set_title(col, fontsize=subtitles_fontsize)
        min = np.floor(df[col].min())
        max = np.ceil(df[col].max())
        xticks = get_ticks(min, max, n_ticks=n_xticks, n_round=n_round_xticks)
        ax.set_xticks(xticks)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.set_xlabel(col)
        ax.set_ylabel('')

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(quant_col_names), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()

######################################################################################################################

def barplot(X, color, categories_order=None, figsize=(9,5), xticks_rotation=0, random=False, 
            n=None, fraction=None, seed=123, fontsize=10, y_up_limit=1, 
            y_low_limit=0, xticks_fontsize=11, yticks_fontsize=11, xlabel_size=11, 
            ylabel_size=11, ylabel='Relative Frequency', xlabel='',
            title_size=14, title_weight='bold') :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    color: name of the color to be use for the histogram bars.
    categories_order: a list with X categories order as they will appear in the plot.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A bar-plot of X variable, with the parameters specified.
    """

    # To use this plot we need a Pandas series, 
    # because X.value_counts(normalize=True).reindex(categories_order) 
    # doesn't work well with Polars.

    if random == True :
        X = X.sample(fraction=fraction, n=n, seed=seed)

    if isinstance(X, pl.Series):
        X = X.to_pandas()

    # Setting the figure size.
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the barplot.
    value_counts = X.value_counts(normalize=True).reindex(categories_order)
    ax = value_counts.plot(kind='bar', color=color)

    ax.set_ylabel(ylabel, size=ylabel_size)
    ax.set_xlabel(xlabel, size=xlabel_size)
    plt.xticks(fontsize=xticks_fontsize, rotation=xticks_rotation)
    plt.yticks(fontsize=yticks_fontsize)

    # Setting the title of the plot.
    plt.title(label = 'Bar-plot' + '  ' + X.name, fontsize=title_size, weight=title_weight)
    ax.set_ylim(y_low_limit, y_up_limit)  

    # Add text annotations to each bar
    for i, v in enumerate(value_counts):
        plt.text(i, v, f"{v:.2f}", color='black', ha='center', va='bottom', fontsize=fontsize, fontweight='bold')

    plt.show()


######################################################################################################################

def barplot_matrix(df, n_cols, title, figsize=(15,15), auto_col=False, 
                    cat_col_names=[], remove_columns=[], add_columns=[], 
                    title_fontsize=15, subtitles_fontsize=12, save=False, file_name=None, orientation='vertical',
                    random=False, n=None, fraction=None, seed=123, x_rotation=0, y_rotation=0, title_height=0.95,
                    style='whitegrid', hspace=1, wspace=0.5, n_yticks=4, n_xticks=4, n_round_yticks=2, n_round_xticks=2,
                    title_weight='bold', subtitles_weight='bold', bar_width=0.3, ylabel_size=11, 
                    xlabel_size=11, xticks_size=10, yticks_size=10, order=None) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).=
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Selecting automatically the categorical columns.
    if auto_col == True :
        cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])

        if len(remove_columns) > 0 :
            for r in remove_columns :
                cat_col_names.remove(r)

        if len(add_columns) > 0 : 
            for r in add_columns :
                cat_col_names.append(r)

    if order is None:
        order = {col: None for col in cat_col_names}
   
    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cat_col_names) / n_cols))
    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  
    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(cat_col_names))

    # Defining a bar-plot for each variable considered.
    for (i, col), color in zip(enumerate(cat_col_names), colors) :
       
        X = df[col].drop_nulls().to_numpy()
        unique_values, rel_freq = get_frequencies(X)
        unique_values = [str(x) for x in unique_values]           
        #proportions = X.value_counts(normalize=True).sort_index()
        #value_counts.plot(kind='bar', color=color, ax=ax)
        if orientation == 'vertical':
            sns.barplot(x=unique_values, y=rel_freq, color=color, width=bar_width, order=order[col], ax=axes[i])
            axes[i].set_xlabel(col, size=xlabel_size)
            axes[i].set_ylabel('Proportion', size=ylabel_size)
            yticks = get_ticks(0, np.max(rel_freq), n_ticks=n_yticks, n_round=n_round_yticks)
            axes[i].set_yticks(yticks)

        elif orientation == 'horizontal':
            sns.barplot(x=rel_freq, y=unique_values, color=color, width=bar_width, order=order[col], ax=axes[i])
            axes[i].set_xlabel('Proportion', size=xlabel_size)
            axes[i].set_ylabel(col, size=ylabel_size)
            xticks = get_ticks(0, np.max(rel_freq), n_ticks=n_xticks, n_round=n_round_xticks)
            axes[i].set_xticks(xticks)
        axes[i].set_title(col, fontsize=subtitles_fontsize, weight=subtitles_weight)
        axes[i].tick_params(axis='x', rotation=x_rotation, labelsize=xticks_size)
        axes[i].tick_params(axis='y', rotation=y_rotation, labelsize=yticks_size)
        for label in axes[i].get_yticklabels():
            #label.set_weight('bold')
            label.set_color('black') 

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cat_col_names), n_rows * n_cols):
        fig.delaxes(axes[j])
    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height, weight=title_weight)
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()

######################################################################################################################

def scatterplot(X, Y, color, figsize=(9,5), n_xticks=10, n_yticks=10, x_rotation=0,   
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid') :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :     
        X = X.sample(fraction=fraction, n=n, seed=seed)
        Y = Y.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the histogram.
    p = sns.scatterplot(x=X, y=Y, color=color)

    # Setting the sticks for x-axis.
    X_min = np.floor(X.min())
    X_max = np.ceil(X.max())
    xticks_index = np.unique(np.round(np.linspace(X_min, X_max, n_xticks)))
    plt.xticks(xticks_index, rotation=x_rotation) 
    
    # Setting the sticks for y-axis.
    Y_min = np.floor(Y.min())
    Y_max = np.ceil(Y.max())
    yticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_yticks)))
    plt.yticks(yticks_index, rotation=x_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'Scatter'+' - '+ X.name + '-' + Y.name, fontsize=15)
    
    if save == True :
        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()


######################################################################################################################

def scatterplot_matrix(df, n_cols, title, figsize=(15,15), auto_col=False, 
                     response=None, predictors=None,
                     quant_col_names=[], remove_columns=[], add_columns=[], 
                     n_xticks=10, n_yticks=10, title_fontsize=15, subtitles_fontsize=12, save=False, file_name=None, 
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, y_rotation=0,
                     title_height=0.95, style='whitegrid', hspace=1, wspace=0.2, n_round_xticks=2, n_round_yticks=2) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)


    if response != None and predictors != None : 

        cols_combis = list(product(predictors, response))

    else :

        # Selecting automatically the quantitative columns.
        if auto_col == True :
            quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])

            if len(remove_columns) > 0 :
                for r in remove_columns :
                    quant_col_names.remove(r)

            if len(add_columns) > 0 : 
                for r in add_columns :
                    quant_col_names.append(r)
   
        cols_combis = list(combinations(quant_col_names, 2))


    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cols_combis) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(cols_combis))

    # Defining a ecdf-plot for each variable considered.
    for (i, (col1, col2)), color in zip(enumerate(cols_combis), colors) :
        
        ax = axes[i]  # Get the current axis
        X = df.select(col1).to_numpy().flatten()
        Y = df.select(col2).to_numpy().flatten()
        sns.scatterplot(x=X, y=Y, color=color, ax=ax)
        ax.set_title(col2 + ' vs ' + col1, fontsize=subtitles_fontsize)
        X_min = np.floor(df[col1].min())
        X_max = np.ceil(df[col1].max())
        Y_min = np.floor(df[col2].min())
        Y_max = np.ceil(df[col2].max())  
        xticks = get_ticks(X_min, X_max, n_ticks=n_xticks, n_round=n_round_xticks)
        yticks = get_ticks(Y_min, Y_max, n_ticks=n_yticks, n_round=n_round_yticks)
        ax.set_yticks(yticks)
        ax.set_xticks(xticks)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.tick_params(axis='y', rotation=y_rotation)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cols_combis), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

######################################################################################################################

def stripplot(df, X_name, Y_name, color, jitter=0.15, figsize=(9,5), n_yticks=10, x_rotation=0,   
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid', size=3, statistics=None, lines_width=0.55, bbox_to_anchor=(0.5,-0.5), legend_size=10,
              color_stats=None) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :     
        df = df.sample(fraction=fraction, n=n, seed=seed)

    X = df[X_name]
    Y = df[Y_name]

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the plot.
    p = sns.stripplot(x=X, y=Y, color=color, jitter=jitter, size=size)

    # Setting the sticks for x-axis.
    plt.xticks(rotation=x_rotation) 
    
    # Setting the sticks for y-axis.
    Y_min = np.floor(Y.min())
    Y_max = np.ceil(Y.max())
    yticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_yticks)))
    plt.yticks(yticks_index, rotation=x_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'Stripplot'+' - '+ Y.name + ' vs ' + X.name, fontsize=15)

    if statistics is not None :

        n_statistics = len(statistics)
        median, median[Y_name], median[Y_name][X_name] = {}, {}, {}
        mean, mean[Y_name], mean[Y_name][X_name] = {}, {}, {}
        if color_stats is None:
            color_stats = sns.color_palette("tab10", n_statistics*len(df[X_name].unique()))
        color_dict = {stat : color for color, stat in zip(color_stats, statistics)}
        #stats_labels = []

        # Get the x-axis category positions
        category_labels = p.get_xticklabels()  # This gives the order seaborn is using for categories
        category_positions = p.get_xticks()
        pos_dict = {label.get_text(): pos for label, pos in zip(category_labels, category_positions)}
    
        for i, cat in enumerate(df[X_name].unique()) :
           cat_pos = pos_dict[str(cat)]   
           width_of_category = lines_width  # Adjust as necessary to match the width of your categories

           if 'median' in statistics :
               median[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].median()
               plt.hlines(y=median[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['median'], linestyles='dashed', label=f'median_{cat}', zorder=4)
               #stats_labels.append(f'median_{Y_name}_{X_name}={cat}')

           if 'mean' in statistics :
               mean[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].mean()
               plt.hlines(y=mean[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['mean'], linestyles='dashed', label=f'mean_{cat}', zorder=4)
               #stats_labels.append(f'mean_{Y_name}_{X_name}={cat}') 

        handles, _ = p.get_legend_handles_labels()
        plt.legend(handles=handles, labels=statistics,  loc='lower center', bbox_to_anchor=bbox_to_anchor, 
                      ncol=n_statistics, fontsize=legend_size)

    if save == True :
        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()


######################################################################################################################


def stripplot_matrix(df, n_cols, title, figsize=(15,15), auto_col=False, 
                     response=None, predictors=None, quant_col_names=[], cat_col_names=[], remove_quant_col=[], add_quant_col=[], 
                     remove_cat_col=[], add_cat_col=[], jitter=0.10, size=3.5, n_yticks=10, 
                     title_fontsize=15, subtitles_fontsize=12, save=False, file_name=None,
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, y_rotation=0,
                     title_height=0.95, style='whitegrid', hspace=1, wspace=0.2, statistics=None, lines_width=0.5, 
                     bbox_to_anchor=(0.5,-1), legend_size=9, color_stats=None, n_round_yticks=2) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    if response != None and predictors != None :

        cols_combis = list(product(predictors, response))

    else :

        # Selecting automatically the quantitative columns.
        if auto_col == True :
            quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])
            cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])

            if len(remove_quant_col) > 0 :
                for r in remove_quant_col :
                   quant_col_names.remove(r)

            if len(remove_cat_col) > 0 :
                for r in remove_cat_col :
                   cat_col_names.remove(r)
                
            if len(add_quant_col) > 0 : 
                for r in add_quant_col :
                    quant_col_names.append(r)

            if len(add_cat_col) > 0 : 
                for r in add_cat_col :
                    cat_col_names.append(r)

        cols_combis = list(product(cat_col_names, quant_col_names))


    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cols_combis) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(cols_combis))

    # Defining a ecdf-plot for each variable considered.
    for (i, (col1, col2)), color in zip(enumerate(cols_combis), colors) :
        
        ax = axes[i]  # Get the current axis
        X = df.select(col1).to_numpy().flatten()
        Y = df.select(col2).to_numpy().flatten()
        sns.stripplot(x=X, y=Y, color=color, jitter=jitter, size=size, ax=ax)
        ax.set_title(col2 + ' vs ' + col1, fontsize=subtitles_fontsize)
        Y_min = np.floor(df[col2].min())
        Y_max = np.ceil(df[col2].max()) 
        yticks = get_ticks(Y_min, Y_max, n_ticks=n_yticks, n_round=n_round_yticks)
        ax.set_yticks(yticks)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.tick_params(axis='y', rotation=y_rotation)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)

        if statistics is not None :

            X_name = col1 ; Y_name = col2
            n_statistics = len(statistics)
            median, median[Y_name], median[Y_name][X_name] = {}, {}, {}
            mean, mean[Y_name], mean[Y_name][X_name] = {}, {}, {}
            if color_stats is None:
                color_stats = sns.color_palette("tab10", n_statistics*len(df[X_name].unique()))
            color_dict = {stat : color for color, stat in zip(color_stats, statistics)}
            #stats_labels = []

            # Get the x-axis category positions
            category_labels = ax.get_xticklabels()  # This gives the order seaborn is using for categories
            category_positions = ax.get_xticks()
            pos_dict = {label.get_text(): pos for label, pos in zip(category_labels, category_positions)}
    
            for cat in df[X_name].unique() :
                
                cat_pos = pos_dict[str(cat)]   
                width_of_category = lines_width  # Adjust as necessary to match the width of your categories

                if 'median' in statistics :
                    median[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].median()
                    ax.hlines(y=median[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['median'], linestyles='dashed', label=f'median_{cat}', zorder=4)
                    ax.get_legend().remove() 

                if 'mean' in statistics :
                   mean[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].mean()
                   ax.hlines(y=mean[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['mean'], linestyles='dashed', label=f'mean_{cat}', zorder=4)
                   #ax.get_legend().remove() 

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cols_combis), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    handles, labels = ax.get_legend_handles_labels() 
    fig.legend(handles, statistics, loc='lower center', bbox_to_anchor=bbox_to_anchor, ncol=len(statistics), fontsize=legend_size)

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

######################################################################################################################

def boxplot_2D(df, X_name, Y_name, color, figsize=(9,5), n_yticks=10, x_rotation=0,   
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid', statistics=None, lines_width=0.55, bbox_to_anchor=(0.5,-0.5), legend_size=10,
              color_stats=None) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :     
        df = df.sample(fraction=fraction, n=n, seed=seed)

    X = df[X_name]
    Y = df[Y_name]

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)

    # Computing the plot.
    p = sns.boxplot(x=X, y=Y, color=color)

    # Setting the sticks for x-axis.
    plt.xticks(rotation=x_rotation) 
    
    # Setting the sticks for y-axis.
    Y_min = np.floor(Y.min())
    Y_max = np.ceil(Y.max())
    yticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_yticks)))
    plt.yticks(yticks_index, rotation=x_rotation) 

    # Setting the title of the plot.
    plt.title(label = 'Boxplot'+' - '+ Y.name + ' vs ' + X.name, fontsize=15)

    if statistics is not None :

        n_statistics = len(statistics)
        median, median[Y_name], median[Y_name][X_name] = {}, {}, {}
        mean, mean[Y_name], mean[Y_name][X_name] = {}, {}, {}
        if color_stats is None:
            color_stats = sns.color_palette("tab10", n_statistics*len(df[X_name].unique()))
        color_dict = {stat : color for color, stat in zip(color_stats, statistics)}
        #stats_labels = []

        # Get the x-axis category positions
        category_labels = p.get_xticklabels()  # This gives the order seaborn is using for categories
        category_positions = p.get_xticks()
        pos_dict = {label.get_text(): pos for label, pos in zip(category_labels, category_positions)}
    
        for cat in df[X_name].unique() :
           cat_pos = pos_dict[str(cat)]   
           width_of_category = lines_width  # Adjust as necessary to match the width of your categories

           if 'median' in statistics :
               median[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].median()
               plt.hlines(y=median[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['median'], linestyles='dashed', label=f'median_{cat}', zorder=4)
               #stats_labels.append(f'median_{Y_name}_{X_name}={cat}')

           if 'mean' in statistics :
               mean[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].mean()
               plt.hlines(y=mean[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['mean'], linestyles='dashed', label=f'mean_{cat}', zorder=4)
               #stats_labels.append(f'mean_{Y_name}_{X_name}={cat}') 

        handles, _ = p.get_legend_handles_labels()
        plt.legend(handles=handles, labels=statistics,  loc='lower center', bbox_to_anchor=bbox_to_anchor, 
                      ncol=n_statistics, fontsize=legend_size)

    if save == True :
        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

######################################################################################################################

def boxplot_2D_matrix(df, n_cols, title, figsize=(15,15), auto_col=False, 
                     response=None, predictors=None,
                     quant_col_names=[], cat_col_names=[], remove_quant_col=[], add_quant_col=[], 
                     remove_cat_col=[], add_cat_col=[], n_yticks=10, 
                     title_fontsize=15, subtitles_fontsize=12, save=False, file_name=None, 
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, y_rotation=0,
                     title_height=0.95, style='whitegrid', hspace=1, wspace=0.2, statistics=None, lines_width=0.5, 
                     bbox_to_anchor=(0.5,-1), legend_size=9, color_stats=None, showfliers = True, n_round_yticks=2) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    if response != None and predictors != None : 

        cols_combis = list(product(predictors, response))

    else :

        # Selecting automatically the quantitative columns.
        if auto_col == True :
            quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])
            cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])

            if len(remove_quant_col) > 0 :
                for r in remove_quant_col :
                    quant_col_names.remove(r)

            if len(remove_cat_col) > 0 :
                for r in remove_cat_col :
                   cat_col_names.remove(r)
                
            if len(add_quant_col) > 0 : 
                for r in add_quant_col :
                    quant_col_names.append(r)

            if len(add_cat_col) > 0 : 
                for r in add_cat_col :
                    cat_col_names.append(r)

        cols_combis = list(product(cat_col_names, quant_col_names))


    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cols_combis) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab10", len(cols_combis))

    # Defining a ecdf-plot for each variable considered.
    for (i, (col1, col2)), color in zip(enumerate(cols_combis), colors) :
        
        ax = axes[i]  # Get the current axis
        X = df.select(col1).to_numpy().flatten()
        Y = df.select(col2).to_numpy().flatten()
        sns.boxplot(x=X, y=Y, color=color, showfliers=showfliers, ax=ax)
        ax.set_title(col2 + ' vs ' + col1, fontsize=subtitles_fontsize)
        if showfliers == True :
            Y_min = np.floor(df[col2].min())
            Y_max = np.ceil(df[col2].max())
            yticks = get_ticks(Y_min, Y_max, n_ticks=n_yticks, n_round=n_round_yticks)        
            ax.set_yticks(yticks)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.tick_params(axis='y', rotation=y_rotation)
        ax.set_xlabel(col1)
        ax.set_ylabel(col2)

        if statistics is not None :

            X_name = col1 ; Y_name = col2
            n_statistics = len(statistics)
            median, median[Y_name], median[Y_name][X_name] = {}, {}, {}
            mean, mean[Y_name], mean[Y_name][X_name] = {}, {}, {}
            if color_stats is None:
                color_stats = sns.color_palette("tab10", n_statistics*len(df[X_name].unique()))
            color_dict = {stat : color for color, stat in zip(color_stats, statistics)}
            #stats_labels = []

            # Get the x-axis category positions
            category_labels = ax.get_xticklabels()  # This gives the order seaborn is using for categories
            category_positions = ax.get_xticks()
            pos_dict = {label.get_text(): pos for label, pos in zip(category_labels, category_positions)}
    
            for cat in df[X_name].unique() :
                
                cat_pos = pos_dict[str(cat)]   
                width_of_category = lines_width  # Adjust as necessary to match the width of your categories

                if 'median' in statistics :
                    median[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].median()
                    ax.hlines(y=median[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['median'], linestyles='dashed', label=f'median_{cat}', zorder=4)

                if 'mean' in statistics :
                   mean[Y_name][X_name][cat] = df.filter(pl.col(X_name) == cat)[Y_name].mean()
                   ax.hlines(y=mean[Y_name][X_name][cat], xmin=cat_pos-width_of_category/2, xmax=cat_pos+width_of_category/2, 
                          colors=color_dict['mean'], linestyles='dashed', label=f'mean_{cat}', zorder=4)

            handles, labels = ax.get_legend_handles_labels() 
            fig.legend(handles, statistics, loc='lower center', bbox_to_anchor=bbox_to_anchor, ncol=len(statistics), fontsize=legend_size)

    # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cols_combis), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

#########################################################################################################
    
def histogram_2D(df, quant_column, cat_column, bins=10, figsize=(9,5), n_yticks=5, n_xticks=10, x_rotation=0,   
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid', bbox_to_anchor=(1,1), legend_size=10, transparency=0.8) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :     
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)
    patches = []
    cat_unique_values = df[cat_column].unique()
    colors = sns.color_palette("tab10", len(cat_unique_values))
    
    # Computing the plot.
    for value, color in zip(cat_unique_values, colors):
        Y_cond = df.filter(pl.col(cat_column)==value).select(quant_column).to_numpy().flatten()
        p = sns.histplot(x=Y_cond, bins=bins, color=color, alpha=transparency, stat='proportion')
        patch = mpatches.Patch(color=color, label=value)
        patches.append(patch)
    p.set_title(quant_column + ' vs ' + cat_column, fontsize=13)
    Y_min = np.floor(df[quant_column].min())
    Y_max = np.ceil(df[quant_column].max())        
    xticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_xticks)))
    p.set_xticks(xticks_index)
    p.set_yticks(np.linspace(0, 1, n_yticks))
    p.tick_params(axis='x', rotation=x_rotation)
    p.set_xlabel(quant_column)
    p.set_ylabel('Proportion')
    p.legend(handles=patches, title=cat_column, loc='upper right', bbox_to_anchor=bbox_to_anchor, fontsize=legend_size)
    
    # Setting the title of the plot.
    plt.title(label = 'Histogram '+' - '+ quant_column + ' vs ' + cat_column, fontsize=15)

    if save == True :
        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

######################################################################################################################
    
def histogram_2D_matrix(df, bins, n_cols, title, figsize=(15,15), auto_col=False, 
                     response=None, predictors=None,
                     quant_col_names=[], cat_col_names=[], remove_quant_col=[], add_quant_col=[], 
                     remove_cat_col=[], add_cat_col=[], n_yticks=5, n_xticks=10,
                     title_fontsize=15, subtitles_fontsize=13, save=False, file_name=None, 
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, 
                     title_height=0.95, style='whitegrid', hspace=1, wspace=0.2,   
                     bbox_to_anchor=(1,1), legend_size=10, transparency=0.8) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    if response != None and predictors != None : 

        cols_combis = list(product(predictors, response))

    else :

        # Selecting automatically the quantitative columns.
        if auto_col == True :
            quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])
            cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])

            if len(remove_quant_col) > 0 :
                for r in remove_quant_col :
                    quant_col_names.remove(r)

            if len(remove_cat_col) > 0 :
                for r in remove_cat_col :
                   cat_col_names.remove(r)
                
            if len(add_quant_col) > 0 : 
                for r in add_quant_col :
                    quant_col_names.append(r)

            if len(add_cat_col) > 0 : 
                for r in add_cat_col :
                    cat_col_names.append(r)

        cols_combis = list(product(cat_col_names, quant_col_names))


    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cols_combis) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab20", 20)

    # Defining a ecdf-plot for each variable considered.
    for i, (col1, col2) in enumerate(cols_combis) :

        patches = []
        ax = axes[i]  # Get the current axis
        #X = df.select(col1).to_numpy().flatten()
        sorted_unique_values = np.sort(df[col1].unique())
        for value, color in zip(sorted_unique_values, colors):
            Y_cond = df.filter(pl.col(col1)==value).select(col2).to_numpy().flatten()
            sns.histplot(x=Y_cond, stat="proportion", bins=bins, color=color, ax=ax, alpha=transparency)
            patch = mpatches.Patch(color=color, label=value)
            patches.append(patch)
        ax.set_title(col2 + ' vs ' + col1, fontsize=subtitles_fontsize)
        Y_min = np.floor(df[col2].min())
        Y_max = np.ceil(df[col2].max())        
        xticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_xticks)))
        ax.set_yticks(np.linspace(0, 1, n_yticks))
        ax.set_xticks(xticks_index)
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.set_xlabel(col2)
        ax.set_ylabel('Proportion')
        ax.legend(handles=patches, title=col1, loc='upper right', bbox_to_anchor=bbox_to_anchor, fontsize=legend_size)

     # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cols_combis), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

#########################################################################################################
    
def ecdfplot_2D(df, quant_column, cat_column, complementary=False, figsize=(9,5), n_yticks=5, n_xticks=10, x_rotation=0,   
              random=False, n=None, fraction=None, seed=123, save=False, file_name=None,
              style='whitegrid', bbox_to_anchor=(1,1), legend_size=10,
              transparency=0.8) :

    """
    Parameters (inputs)
    ----------
    X: a pandas series or a numpy array (the variable).
    bins: number of intervals used to create the histogram (number of bars).
    color: name of the color to be use for the histogram bars.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    rotation: a integer positive number. Indicates the rotation degree of the sticks from the axis.
    get_intervals:If True, the intervals used to create the histogram will be return. If False, not.
    sep: a parameter used for creating the sticks of the x-axis. We recommend using the default value.
   
    Returns (outputs)
    ----------
    A histogram of X variable, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :     
        df = df.sample(fraction=fraction, n=n, seed=seed)

    # Setting the figure size
    fig, axs = plt.subplots(figsize=figsize)
    patches = []
    cat_unique_values = df[cat_column].unique()
    colors = sns.color_palette("tab10", len(cat_unique_values))
    
    # Computing the plot.
    for value, color in zip(cat_unique_values, colors):
        Y_cond = df.filter(pl.col(cat_column)==value).select(quant_column).to_numpy().flatten()
        p = sns.ecdfplot(x=Y_cond, color=color, alpha=transparency, complementary=complementary)
        patch = mpatches.Patch(color=color, label=value)
        patches.append(patch)
    p.set_title(quant_column + ' vs ' + cat_column, fontsize=13)
    Y_min = np.floor(df[quant_column].min())
    Y_max = np.ceil(df[quant_column].max())        
    xticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_xticks)))
    p.set_xticks(xticks_index)
    p.set_yticks(np.linspace(0, 1, n_yticks))
    p.tick_params(axis='x', rotation=x_rotation)
    p.set_xlabel(quant_column)
    p.set_ylabel('Proportion')
    p.legend(handles=patches, title=cat_column, loc='upper right', bbox_to_anchor=bbox_to_anchor, fontsize=legend_size)
    
    # Setting the title of the plot.
    plt.title(label = 'Ecdfplot'+' - '+ quant_column + ' vs ' + cat_column, fontsize=15)

    if save == True :
        fig.savefig(file_name + '.jpg', format='jpg', dpi=600, bbox_inches="tight")
    
    plt.show()

#########################################################################################################
    
def ecdfplot_2D_matrix(df, n_cols, title, complementary=False, figsize=(15,15), auto_col=False, 
                     response=None, predictors=None,
                     quant_col_names=[], cat_col_names=[], remove_quant_col=[], add_quant_col=[], 
                     remove_cat_col=[], add_cat_col=[], n_yticks=5, n_xticks=10,
                     title_fontsize=15, subtitle_fontsize=12, save=False, file_name=None, 
                     random=False, n=None, fraction=None, seed=123, x_rotation=0, 
                     title_height=0.95, style='whitegrid', hspace=1, wspace=0.2,   
                     bbox_to_anchor=(1,1), legend_size=10, transparency=0.8) :
 
    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data-matrix).
    bins: number of intervals used to create the histogram (number of bars).
    tittle: the tittle of the histogram.
    figsize: dimensions of the plot. Must be a pair of numbers (a,b), where a indicates the plot width, and b the length.
    auto_col: if True, the quantitative columns are selected automatically. If False, the function uses the columns of col_list.
    auto_dim: if True, the matrix-plot dimension is defined automatically. If False, the function uses (n,m) as dimension.
    n, m: number of rows (n) and columns (m) of the matrix-plot, if auto_dim=False.
    col_list: a list with the names of some columns. Only used if auto=False.
    remove_columns: columns to remove to the ones considered if auto=True.
    add_columns:columns to add to the ones considered if auto=True.
    save: if True, the plot will be save as jpg file. If False, not.
    file_name: the name of the jpg file if save=True.
    n_xticks: number of ticks in x-axis.
    fontsize: is the fontsize of the plot tittle.
   
    Returns (outputs)
    ----------
    A histogram matrix of the df data-set, with the parameters specified.
    """

    sns.set_style(style)

    if random == True :
        df = df.sample(fraction=fraction, n=n, seed=seed)

    if response != None and predictors != None : 

        cols_combis = list(product(predictors, response))

    else :

        # Selecting automatically the quantitative columns.
        if auto_col == True :
            quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])
            cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])

            if len(remove_quant_col) > 0 :
                for r in remove_quant_col :
                    quant_col_names.remove(r)

            if len(remove_cat_col) > 0 :
                for r in remove_cat_col :
                   cat_col_names.remove(r)
                
            if len(add_quant_col) > 0 : 
                for r in add_quant_col :
                    quant_col_names.append(r)

            if len(add_cat_col) > 0 : 
                for r in add_cat_col :
                    cat_col_names.append(r)

        cols_combis = list(product(cat_col_names, quant_col_names))


    # Define the number of rows and columns for the matrix plot
    n_rows = int(np.ceil(len(cols_combis) / n_cols))

    # Create a subplot with the specified number of rows and columns
    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)

    # Flatten the axes array to make it easier to iterate
    axes = axes.flatten()  

    # Defining the colors to be used.
    colors = sns.color_palette("tab20", 20)

    # Defining a ecdf-plot for each variable considered.
    for i, (col1, col2) in enumerate(cols_combis) :
        # If response and predictors not None: col1 = predictors ; col2 = response
        # If response and predictors are None: col1 = cat columns ; col2 = quant columns 

        patches = []
        ax = axes[i]  # Get the current axis
        for value, color in zip(df[col1].unique(), colors):
            Y_cond = df.filter(pl.col(col1)==value).select(col2).to_numpy().flatten()
            sns.ecdfplot(x=Y_cond, color=color, ax=ax, alpha=transparency, complementary=complementary)
            patch = mpatches.Patch(color=color, label=value)
            patches.append(patch)
        ax.set_title(col2 + ' vs ' + col1, fontsize=subtitle_fontsize)
        Y_min = np.floor(df[col2].min())
        Y_max = np.ceil(df[col2].max())        
        xticks_index = np.unique(np.round(np.linspace(Y_min, Y_max, n_xticks)))
        ax.set_xticks(xticks_index)
        ax.set_yticks(np.linspace(0, 1, n_yticks))
        ax.tick_params(axis='x', rotation=x_rotation)
        ax.set_xlabel(col2)
        ax.set_ylabel('Proportion')
        ax.legend(handles=patches, title=col1, loc='upper right', bbox_to_anchor=bbox_to_anchor, fontsize=legend_size)

     # Remove any unused subplots in case the number of 'geo' values is less than num_rows * num_cols
    for j in range(len(cols_combis), n_rows * n_cols):
        fig.delaxes(axes[j])

    # Establishing a general tittle for the plot.
    plt.suptitle(title, fontsize=title_fontsize, y=title_height)
    
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 

    # Setting save options.
    if save == True :         
        fig.savefig(file_name + '.jpg', format='jpg', dpi=500)

    plt.show()  

##########################################################################################

# To visualize contingency tables (cat vs cat). 
# Useful when the response is categorical and we want to analyze the influence of categorical predictors on it.


def barplot_2D(df, cat_condition, cat_conditioned, n_rows, figsize, title_size, subtitles_size, title_height, 
               xlabel_size=10, xticks_size=9, hspace=1, wspace=0.5, palette='tab10', ylabel_size=11, x_rotation=0,
               max_ytick=1, title_weight='bold', categories_order=None, bar_width=0.4, alpha=1):
    
    # Condition variable: cat_condition
    # Conditioned variable:cat_response
    cond_prop_response = {cat_condition: {}}
    for cat in df[cat_condition].unique():

        Y_cond = df.filter(pl.col(cat_condition) == cat)[cat_conditioned].to_numpy()
        unique_values, counts = np.unique(Y_cond, return_counts=True)
        prop = np.round(counts / len(Y_cond), 3)
        cond_prop_response[cat_condition][cat] = dict(zip(unique_values, prop))

    n_categories = len(cond_prop_response[cat_condition].keys())
    n_cols = int(np.ceil(n_categories / n_rows))
    fig, axs = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = axs.flatten()
    colors = sns.color_palette(palette, 100)

    for i, cat in enumerate(cond_prop_response[cat_condition]):
        
        categories = list(cond_prop_response[cat_condition][cat].keys())
        proportions = list(cond_prop_response[cat_condition][cat].values())
        sns.barplot(x=categories, y=proportions, color=colors[i],
                    order=categories_order, alpha=alpha, width=bar_width, ax=axes[i])

        axes[i].set_title(cat, fontsize=subtitles_size)
        axes[i].set_ylabel('')
        axes[i].set_xlabel(cat_conditioned, size=xlabel_size)
        axes[i].tick_params(axis='x', rotation=x_rotation, labelsize=xticks_size)
        if max_ytick is not None:
            axes[i].set_yticks(np.arange(0, max_ytick + 0.2, 0.2))
        else:
            max_prop = np.max(proportions)
            axes[i].set_yticks(np.arange(0, max_prop + 0.2, 0.2))
    axes[0].set_ylabel('Proportion', size=ylabel_size)

    plt.suptitle(f'{cat_conditioned} | {cat_condition}', size=title_size, weight=title_weight, y=title_height)
    plt.subplots_adjust(hspace=hspace, wspace=wspace) 
    for j in range(n_categories, n_rows * n_cols):
        fig.delaxes(axes[j])
    plt.show()