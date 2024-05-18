import polars as pl
import pandas as pd
import numpy as np
from scipy.stats import percentileofscore
from scipy.stats import kurtosis as kurtosis_scipy
from scipy.stats import skew
from itertools import combinations, product
from collections import Counter

from BigEDA.preprocessing import columns_names, prop_cols_nulls

######################################################################################################################

def weighted_mean(X,w):

    """
    Parameters (inputs)
    ----------
    X: a Pandas series (the statistical variable).    
    w: an 1-D Numpy array with the weights (the weights vector). 
    
    Returns (outputs)
    -------
    weighted_mean_: the weighted mean of X using w as weights vector, computed using the formula presented above.
    """
    
    if not isinstance(X, np.ndarray) :
        X = X.to_numpy()

    weighted_mean_ = (1/np.sum(w))*np.sum(X*w)

    return weighted_mean_

######################################################################################################################

def inv_quantile(X, h, scipy=False):

    """
    Parameters (inputs)
    ----------
    X: a Polars series (the statistical variable).   
    h: the order of the inverse quantile. Must be a number in the domain of the variable represented by X. 
        
    Returns (outputs)
    -------
    inv_quantile_: the h-order inverse quantile of X.
    """

    if scipy == False:

        inv_quantile_ = round((X <= h).sum() / len(X), 4)

    else:

        inv_quantile_ = round(percentileofscore(X, h), 4)

    return inv_quantile_

######################################################################################################################

def kurtosis(X, scipy=False):

    """
    Parameters (inputs)
    ----------
    X: a Polars series (the statistical variable).    
        
    Returns (outputs)
    -------
    kurtosis_: the kurtosis of X.
    """
    if scipy == False:

        n = len(X)
        X_mean = X.mean()
        X_std = X.std()
        mu4 = (1/n)*((X - X_mean)**4).sum()
        kurtosis_ = mu4/(X_std**4) 

    else:

        kurtosis_ = kurtosis_scipy(X, fisher=False)

    return kurtosis_

######################################################################################################################

def skewness(X, scipy=False):

    """
    Parameters (inputs)
    ----------
    X: a Polars series (the statistical variable).    
        
    Returns (outputs)
    -------
    skewness_: the skewness of X.
    """

    if scipy == False :

        n = len(X)
        X_mean = X.mean()
        X_std = X.std()
        mu3 = (1/n)*((X - X_mean)**3).sum()
        skewness_ = (mu3/(X_std**3))

    else:

        skewness_ = skew(X)

    return skewness_

######################################################################################################################

def MAD(X):

    """
    Parameters (inputs)
    ----------
    X: a Polars series (the statistical variable).    
        
    Returns (outputs)
    -------
    MAD_: the median absolute deviation of X.
    """

    X_median = X.median()
    MAD_ = ((X- X_median).abs()).median()

    return MAD_

######################################################################################################################

def outlier_detection(X, h=1.5) :

    """
    Parameters (inputs)
    ----------
    X: a Polars series (the statistical variable).
    h: a real number >= 0.
        
    Returns (outputs)
    -------
    trimmed_variable: the trimmed X variable, that is, a polars series with the values of X that are not outliers.
    outliers: a polars series with the outliers of X variable.
    """

    if isinstance(X, pl.DataFrame):
        # Transform a pl.DataFrame as pl.Series
        X = X[X.columns[0]]

    Q1 = X.quantile(0.25)
    Q3 = X.quantile(0.75)
    IQR = Q3 - Q1
    upper_bound = Q3 + h*IQR
    lower_bound = Q1 - h*IQR

    trimmed_variable = X.filter((X >= lower_bound) & (X <= upper_bound))
    outliers = X.filter((X < lower_bound) | (X > upper_bound))  

    return trimmed_variable , outliers, lower_bound, upper_bound

######################################################################################################################

def outliers_table(df, auto=True, col_names=[], h=1.5) :

    """
    Parameters (inputs)
    ----------
    df: a polars data-frame (the data matrix).
    auto: can be True or False. If True, quantitative columns are detect automatically. If false, the function use the columns named in cols_list.
    cols_list: a list with the names of the columns that will be used in the case that auto=False.    
    h: a real number >= 0.

    Returns (outputs)
    -------
    df_outliers: a polars data-frame with the number of outliers/not outliers and the proportion of them, for the quantitative variables of df (if auto=True) 
                 or for the  variables of df whom names are in cols_list (if auto=False).
    """

    n_outliers = []
    n_not_outliers = []

    if auto == True : 

        quant_col_names = columns_names(df, types = [pl.Float64, pl.Int64])

    elif auto == False : 

        quant_col_names = col_names
     
    lower_bound_list, upper_bound_list = [], []

    for col in quant_col_names :
        
        trimmed_variable , outliers, lower_bound, upper_bound = outlier_detection(X=df[col], h=h)
        n_outliers.append(len(outliers))
        n_not_outliers.append(len(trimmed_variable))
        lower_bound_list.append(lower_bound)
        upper_bound_list.append(upper_bound)

    df_outliers = pl.DataFrame({'quant_variables': quant_col_names, 'lower_bound': lower_bound_list, 
                                'upper_bound': upper_bound_list, 'n_outliers': n_outliers, 'n_not_outliers': n_not_outliers})
    df_outliers = df_outliers.with_columns([(pl.col('n_outliers') / (pl.col('n_outliers') + pl.col('n_not_outliers'))).alias('prop_outliers')])
    df_outliers = df_outliers.with_columns([(1 - pl.col('prop_outliers')).alias('prop_not_outliers')])

    return df_outliers 

######################################################################################################################

def freq_table(X, intervals=None) :

    # Function to extract the lower bound from each interval
    def extract_lower_bound(interval):
        if interval.startswith("(-inf"):
            return float('-inf')
        else:
            return float(interval.split(", ")[0][1:])

    if intervals == None:
        unique_values, counts = np.unique(X, return_counts=True)
        sorted_indices = np.argsort(counts)
        sorted_intervals = unique_values[sorted_indices]
        counts = counts[sorted_indices]
        rel_counts = counts / len(X)

    if intervals != None :
        unique_values, counts = np.unique(X, return_counts=True)
        lower_bounds = np.array([extract_lower_bound(interval) for interval in unique_values])
        unique_values_sorted_indices = np.argsort(lower_bounds)
        sorted_intervals = unique_values[unique_values_sorted_indices]
        counts = counts[unique_values_sorted_indices]
        rel_counts = counts / len(X)
        intervals_dict = dict()
        for x, int in enumerate(intervals):
            intervals_dict[int] = x
        intervals_not_null = [int for int in intervals if intervals_dict[int] in sorted_intervals]
        unique_values = intervals_not_null


    if isinstance(X, (np.ndarray, list)):

        title = 'unique values'

    else :

        title = X.name + ': unique values'

    freq_df = pl.DataFrame({title : sorted_intervals, 
                                'abs_freq' : counts, 
                                'rel_freq' : np.round(rel_counts, 4), 
                                'cum_abs_freq' : np.cumsum(counts), 
                                'cum_rel_freq' : np.cumsum(rel_counts)})
         

    return freq_df

######################################################################################################################

def summary(df, auto_col=False, quant_col_names=[], cat_col_names=[]) :

    if auto_col == True :
        quant_col_names = columns_names(df, types=[pl.Float64, pl.Int64])
        cat_col_names = columns_names(df, types=[pl.Boolean, pl.Utf8])

    elif auto_col == False : 
        # colnames debe ser un objeto tipo colnames = [list_quant_columns , list_cat_columns]
        # Ejemplo: colnames = [['quant_1' , 'quant_2'], ['cat_1', 'cat_2', 'cat_3']]
        quant_col_names = quant_col_names
        cat_col_names = cat_col_names

    n_rows = len(df)

    if len(quant_col_names) > 0 :
         
        # mean_quant_cols = [df[col].mean() for col in quant_col_names]
        mean_quant_cols = df[quant_col_names].mean().to_numpy().flatten()
        # std_quant_cols = [df[col].std() for col in quant_col_names]
        std_quant_cols = df[quant_col_names].std().to_numpy().flatten()
        # median_quant_cols = [df[col].median() for col in quant_col_names]
        median_quant_cols = df[quant_col_names].median().to_numpy().flatten()
        # Q25_quant_cols = [df[col].quantile(0.10) for col in quant_col_names]
        Q25_quant_cols = df[quant_col_names].quantile(0.25).to_numpy().flatten()
        # Q10_quant_cols = [df[col].quantile(0.25) for col in quant_col_names]
        Q10_quant_cols = df[quant_col_names].quantile(0.10).to_numpy().flatten()
        # Q75_quant_cols = [df[col].quantile(0.75) for col in quant_col_names]
        Q75_quant_cols = df[quant_col_names].quantile(0.75).to_numpy().flatten()
        # Q90_quant_cols = [df[col].quantile(0.90) for col in quant_col_names]
        Q90_quant_cols = df[quant_col_names].quantile(0.90).to_numpy().flatten()
        # max_quant_cols = [df[col].max() for col in quant_col_names]
        max_quant_cols = df[quant_col_names].max().to_numpy().flatten()
        # min_quant_cols = [df[col].min() for col in quant_col_names]
        min_quant_cols = df[quant_col_names].min().to_numpy().flatten()
        kurtosis_quant_cols = [kurtosis(df[col], scipy=True) for col in quant_col_names]
        skewness_quant_cols = [skewness(df[col], scipy=True) for col in quant_col_names]

        prop_outliers = []
        for col in quant_col_names :
           _, outliers, _, _ = outlier_detection(X=df[col], h=1.5)
           prop_outliers.append(len(outliers)/n_rows)

        num_unique_values_quant_col = []
        for col in quant_col_names :
            unique_values = df[col].unique().to_numpy()
            unique_values = [x for x in unique_values if x is not None]
            num_unique_values_quant_col.append(len(unique_values))

        prop_nulls_quant_cols = prop_cols_nulls(df[quant_col_names])

        quant_summary = pd.DataFrame(index=quant_col_names, 
                                    columns=['n_unique', 'prop_nan', 'mean','std','min','Q10','Q25','median','Q75', 'Q90','max', 
                                             'kurtosis', 'skew', 'prop_outliers'])

        quant_summary.loc[:,'n_unique'] = num_unique_values_quant_col
        quant_summary.loc[:,'prop_nan'] = prop_nulls_quant_cols
        quant_summary.loc[:,'mean'] = mean_quant_cols
        quant_summary.loc[:,'std'] = std_quant_cols
        quant_summary.loc[:,'min'] = min_quant_cols
        quant_summary.loc[:,'Q10'] = Q10_quant_cols
        quant_summary.loc[:,'Q25'] = Q25_quant_cols
        quant_summary.loc[:,'median'] = median_quant_cols 
        quant_summary.loc[:,'Q75'] = Q75_quant_cols
        quant_summary.loc[:,'Q90'] = Q90_quant_cols
        quant_summary.loc[:,'max'] = max_quant_cols
        quant_summary.loc[:,'kurtosis'] = kurtosis_quant_cols
        quant_summary.loc[:,'skew'] = skewness_quant_cols
        quant_summary.loc[:,'prop_outliers'] = prop_outliers

    else :

        quant_summary = None


    if len(cat_col_names) > 0 :

        mode_cat_cols = [df[col].mode()[0] for col in cat_col_names]

        num_unique_values_cat_col = []
        for col in cat_col_names :
            unique_values = df[col].unique().to_numpy()
            unique_values = [x for x in unique_values if x is not None]
            num_unique_values_cat_col.append(len(unique_values))

        prop_nulls_cat_cols = prop_cols_nulls(df[cat_col_names])

        cat_summary = pd.DataFrame(index=cat_col_names, 
                                   columns=['n_unique', 'prop_nan', 'mode'])

        cat_summary.loc[:,'n_unique'] = num_unique_values_cat_col
        cat_summary.loc[:,'prop_nan'] = prop_nulls_cat_cols
        cat_summary.loc[:,'mode'] = mode_cat_cols

    else :

        cat_summary = None
  
    return quant_summary, cat_summary

######################################################################################################################

def cross_quant_cat_summary(df, quant_col, cat_col) :

    quant_cond_summary = df.group_by(cat_col).agg([
           (pl.col(quant_col).count() / len(df)).alias(f'prop_{quant_col}'),
            pl.col(quant_col).mean().alias(f'mean_{quant_col}'),
            pl.col(quant_col).std().alias(f'std_{quant_col}'),
            pl.col(quant_col).min().alias(f'min_{quant_col}'),
            pl.col(quant_col).quantile(0.10).alias(f'Q10_{quant_col}'),
            pl.col(quant_col).quantile(0.25).alias(f'Q25_{quant_col}'),
            pl.col(quant_col).median().alias(f'median_{quant_col}'),
            pl.col(quant_col).quantile(0.75).alias(f'Q75_{quant_col}'),
            pl.col(quant_col).quantile(0.90).alias(f'Q90_{quant_col}'),
            pl.col(quant_col).max().alias(f'max_price'),
            pl.col(quant_col).kurtosis().alias(f'kurtosis_{quant_col}'),
            pl.col(quant_col).skew().alias(f'skew_{quant_col}')
            ])
    
    quant_cond_summary = quant_cond_summary.filter(pl.col(cat_col).is_not_null())
    summary_columns = quant_cond_summary.columns
    quant_cond_summary_cat_col = quant_cond_summary[:,0].to_numpy()
    quant_cond_summary_rest = np.round(quant_cond_summary[:,1:].to_numpy(), 3)
    quant_cond_summary =  pl.from_numpy(np.column_stack((quant_cond_summary_cat_col, quant_cond_summary_rest)))
    quant_cond_summary.columns = summary_columns

    unique_values = df[cat_col].unique().to_numpy()
    unique_values = [x for x in unique_values if x is not None]

    df_cond = {quant_col: {cat_col : {}}} 
    for cat in unique_values :
        df_cond[quant_col][cat_col][cat] = df.filter(pl.col(cat_col) == cat)[quant_col]

    prop_outliers_dict = dict()
    for cat in unique_values:
        trimmed_variable , outliers, lower_bound, upper_bound = outlier_detection(X=df_cond[quant_col][cat_col][cat], h=1.5)
        prop_outliers_dict[cat] = len(outliers)/len(df_cond[quant_col][cat_col][cat])

    prop_outliers = pl.Series(prop_outliers_dict.values())
    # prop_not_outliers = pl.Series(prop_not_outliers_dict.values())
    quant_cond_summary = quant_cond_summary.with_columns(prop_outliers.alias(f'prop_outliers_{quant_col}'))
    # quant_cond_summary = quant_cond_summary.with_columns(prop_not_outliers.alias('prop_not_outliers_buy_price'))

    prop_nulls_dict = dict()
    # prop_not_nulls_dict = dict()
    for cat in unique_values:
        prop_nulls_dict[cat] = prop_cols_nulls(df_cond[quant_col][cat_col][cat])
        # prop_not_nulls_dict[cat] = 1 - prop_nulls_dict[cat]

    prop_nulls = pl.Series(prop_nulls_dict.values())
    # prop_not_nulls = pl.Series(prop_not_nulls_dict.values())
    quant_cond_summary = quant_cond_summary.with_columns(prop_nulls.alias(f'prop_nan_{quant_col}'))
    # quant_cond_summary = quant_cond_summary.with_columns(prop_not_nulls.alias('prop_not_nan_buy_price'))
    if df[cat_col].dtype in [pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
        quant_cond_summary = quant_cond_summary.sort(by=quant_cond_summary.columns[0])

    return quant_cond_summary

######################################################################################################################

def contingency_table_2D(df, cat1_name, cat2_name, conditional=False, axis=1) :

    # axis = 0: cat1 is the conditioning variable
    # axis = 1: cat2 is the conditioning variable

    if conditional == False :

       cat1_array = df[cat1_name].to_numpy().flatten()
       cat2_array = df[cat2_name].to_numpy().flatten()
       cat12_list = [(x,y) for (x,y) in zip(cat1_array, cat2_array)]

       count_dict = Counter(cat12_list)
       unique_values = count_dict.keys()
       counts = np.array([x for x in count_dict.values()])

       rel_counts = counts / len(df)
       name = f'({cat1_name}, {cat2_name}) : unique values'

       
       contigency_table_df = pl.DataFrame({name : unique_values, 
                                           'abs_freq' : counts, 
                                           'rel_freq' : np.round(rel_counts, 4), 
                                           'cum_abs_freq' : np.cumsum(counts), 
                                           'cum_rel_freq' : np.cumsum(rel_counts)})   

    elif conditional == True :

        cat12_cond = dict()
    
        if axis == 0 : 

            for cat in  np.unique(df[cat1_name]) :
                cat12_cond[cat] = df.filter(pl.col(cat1_name) == cat)[cat2_name]
            
            cat12_list = list()
            for cat in  np.unique(df[cat1_name]) :
                cat12_list = cat12_list + [(x,y) for (x,y) in product(cat12_cond[cat], [cat])]  

            count_dict = Counter(cat12_list)
            unique_values = count_dict.keys()
            counts = [x for x in count_dict.values()]
            rel_counts = list()
            for cat in np.unique(df[cat1_name]):
                rel_counts = rel_counts + [x / len(cat12_cond[cat]) for x,y in zip(count_dict.values(), count_dict.keys()) if y[1] == cat]
            name = f'({cat2_name} | {cat1_name}) : unique values'
        
        elif axis == 1 :

            for cat in  np.unique(df[cat2_name]) :
                cat12_cond[cat] = df.filter(pl.col(cat2_name) == cat)[cat1_name]
            
            cat12_list = list()
            for cat in  np.unique(df[cat2_name]) :
                cat12_list = cat12_list + [(x,y) for (x,y) in product(cat12_cond[cat], [cat])]  

            count_dict = Counter(cat12_list)
            unique_values = count_dict.keys()
            counts = np.array([x for x in count_dict.values()])
            rel_counts = list()
            for cat in np.unique(df[cat2_name]):
                rel_counts = rel_counts + [x / len(cat12_cond[cat]) for x,y in zip(count_dict.values(), count_dict.keys()) if y[1] == cat]         
            name = f'({cat1_name} | {cat2_name}) : unique values'


        contigency_table_df = pl.DataFrame({name : unique_values, 
                                           'abs_freq' : counts, 
                                           'rel_freq' : np.round(rel_counts, 4)})     
    
    return contigency_table_df

######################################################################################################################


def contingency_table_3D(df, cat1_name, cat2_name, cat3_name, conditional=False, axis=[1,2]) :

    if conditional == False :

       cat1_array = df[cat1_name].to_numpy().flatten()
       cat2_array = df[cat2_name].to_numpy().flatten()
       cat3_array = df[cat3_name].to_numpy().flatten()
       cat123_list = [(x,y,z) for (x,y,z) in zip(cat1_array, cat2_array, cat3_array)]

       count_dict = Counter(cat123_list)
       unique_values = count_dict.keys()
       counts = np.array([x for x in count_dict.values()])

       rel_counts = counts / len(df)
       name = f'({cat1_name}, {cat2_name}, {cat3_name}) : unique values'

       
       contigency_table_df = pl.DataFrame({name : unique_values, 
                                           'abs_freq' : counts, 
                                           'rel_freq' : np.round(rel_counts, 4), 
                                           'cum_abs_freq' : np.cumsum(counts), 
                                           'cum_rel_freq' : np.cumsum(rel_counts)})   

    elif conditional == True :

        cat123_cond = dict()
    
        if axis == [0,1] or axis == [1,0]: 

            cat123_cond = dict()

            for cat in  product(np.unique(df[cat1_name]), np.unique(df[cat2_name])) :
                cat123_cond[cat] = df.filter((pl.col(cat1_name) == cat[0]) & (pl.col(cat2_name) == cat[1]))[cat3_name]
        
            cat123_list = list()
            for cat in  product(np.unique(df[cat1_name]), np.unique(df[cat2_name])) :
                cat123_list = cat123_list + [(x,y,z) for x,(y,z) in product(cat123_cond[cat], [cat])]  

            count_dict = Counter(cat123_list)
            unique_values = count_dict.keys()
            counts = [x for x in count_dict.values()]
            rel_counts = list()

            for cat in product(np.unique(df[cat1_name]), np.unique(df[cat2_name])) :
                rel_counts = rel_counts + [x / len(cat123_cond[cat]) for x,y in zip(count_dict.values(), count_dict.keys()) if y[1:3] == cat]

            name = f'({cat3_name} | {cat1_name} , {cat2_name}) : unique values'
        
        if axis == [0,2] or axis == [2,0] : 

            cat123_cond = dict()

            for cat in  product(np.unique(df[cat1_name]), np.unique(df[cat3_name])) :
                cat123_cond[cat] = df.filter((pl.col(cat1_name) == cat[0]) & (pl.col(cat3_name) == cat[1]))[cat2_name]
        
            cat123_list = list()
            for cat in  product(np.unique(df[cat1_name]), np.unique(df[cat3_name])) :
                cat123_list = cat123_list + [(x,y,z) for x,(y,z) in product(cat123_cond[cat], [cat])]  

            count_dict = Counter(cat123_list)
            unique_values = count_dict.keys()
            counts = [x for x in count_dict.values()]
            rel_counts = list()

            for cat in product(np.unique(df[cat1_name]), np.unique(df[cat3_name])) :
                rel_counts = rel_counts + [x / len(cat123_cond[cat]) for x,y in zip(count_dict.values(), count_dict.keys()) if y[1:3] == cat]

            name = f'({cat2_name} | {cat1_name} , {cat3_name}) : unique values'

        if axis == [1,2] or axis == [2,1] : 

            cat123_cond = dict()

            for cat in  product(np.unique(df[cat2_name]), np.unique(df[cat3_name])) :
                cat123_cond[cat] = df.filter((pl.col(cat2_name) == cat[0]) & (pl.col(cat3_name) == cat[1]))[cat1_name]

            cat123_list = list()
            for cat in  product(np.unique(df[cat2_name]), np.unique(df[cat3_name])) :
                cat123_list = cat123_list + [(x,y,z) for x,(y,z) in product(cat123_cond[cat], [cat])]  

            count_dict = Counter(cat123_list)
            unique_values = count_dict.keys()
            counts = [x for x in count_dict.values()]
            rel_counts = list()

            for cat in product(np.unique(df[cat2_name]), np.unique(df[cat3_name])) :
                rel_counts = rel_counts + [x / len(cat123_cond[cat]) for x,y in zip(count_dict.values(), count_dict.keys()) if y[1:3] == cat]

            name = f'({cat1_name} | {cat2_name} , {cat3_name}) : unique values'


        contigency_table_df = pl.DataFrame({name : unique_values, 
                                           'abs_freq' : counts, 
                                           'rel_freq' : np.round(rel_counts, 4)})     
    
    return contigency_table_df

######################################################################################################################

def cov_matrix(df, auto_col=False, quant_col_names=None) :

    if auto_col == True :
        quant_col_names = columns_names(df, types=[pl.Float64, pl.Int64])

    p_quant = len(quant_col_names)
    cov_matrix_ = np.zeros((p_quant,p_quant))

    for i, col1 in enumerate(quant_col_names) :
        for j, col2 in enumerate(quant_col_names) :
            if j >= i:
               cov_matrix_[i,j] = np.round(df.select(pl.cov(col1, col2)).to_numpy()[0][0], 2)

    cov_matrix_ = cov_matrix_ + np.triu(cov_matrix_, k=1).T

    cov_matrix_df = pd.DataFrame(cov_matrix_, columns=quant_col_names, index=quant_col_names)
    
    return cov_matrix_df

######################################################################################################################

def corr_matrix(df, auto_col=False, quant_col_names=None, response=None, predictors=None, method='pearson') :

    if response != None and predictors != None : 

        corr_list = []
        for col in predictors:
            corr_list.append(np.round(df.select(pl.corr(response, col, method=method)).to_numpy()[0][0], 2))

        corr_list_df = pd.DataFrame(corr_list, columns=[response], index=predictors) 

        return corr_list_df
    
    else :

        if auto_col == True :
            quant_col_names = columns_names(df, types=[pl.Float64, pl.Int64])

        p_quant = len(quant_col_names)
        corr_matrix_ = np.zeros((p_quant,p_quant))

        for i, col1 in enumerate(quant_col_names) :
            for j, col2 in enumerate(quant_col_names) :
                if j >= i:
                    corr_matrix_[i,j] = np.round(df.select(pl.corr(col1, col2, method=method)).to_numpy()[0][0], 2)

        corr_matrix_ = corr_matrix_ + np.triu(corr_matrix_, k=1).T

        corr_matrix_df = pd.DataFrame(corr_matrix_, columns=quant_col_names, index=quant_col_names) 
       
        return corr_matrix_df

######################################################################################################################
    
def high_corr(df, upper, lower, auto_col=False, quant_col_names=None, method='pearson'):

    if auto_col == True :
        quant_col_names = columns_names(df, types=[pl.Float64, pl.Int64])

    corr_dict = dict()

    for (col1,col2) in combinations(quant_col_names, 2) :
   
       corr = np.round(df.select(pl.corr(col1, col2, method=method)).to_numpy()[0][0], 2)
   
       if corr >= upper or corr <= lower :
      
          corr_dict[str((col1,col2))] = corr

    high_corr_df = pd.DataFrame(corr_dict, index=['corr'])

    return high_corr_df
    
######################################################################################################################
