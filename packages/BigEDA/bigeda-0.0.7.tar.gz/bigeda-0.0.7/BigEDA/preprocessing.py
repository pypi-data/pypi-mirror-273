######################################################################################################################

import polars as pl
import pandas as pd
import numpy as np
import random

######################################################################################################################

def dtypes_df(df):
    
    """
    Parameters (inputs)
    ----------
    df: a Polars data-frame.     

    Returns (outputs)
    -------
    Python_types_df: a Polars data-frame with the Python type of each column (variable) of df data-frame.
    """

    Python_types_df = pl.DataFrame({'Columns' : df.columns, 'Python_type' : df.dtypes})

    return Python_types_df


def change_type(df, col_name, new_type) :

    """
    Parameters (inputs)
    ----------
    df: a Polars data-frame.    
    col: the name of a column from df. 
    new_type: the name of the Python type that you want to set for col_name. 

    Returns (outputs)
    -------
    The function changes the type of the col_name column of the df data-frame to new_type.
    """

    return df.with_columns(df[col_name].cast(new_type))    

######################################################################################################################

def columns_names(df, types=[pl.Float64, pl.Int64]):

    columns_names_ = [col for col in df.columns 
                            if df.select(pl.col(col)).dtypes[0] in types]
    
    return columns_names_

######################################################################################################################

def outlier_filter(df, col, h=1.5) :

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

    Q3 = df[col].quantile(0.75)
    Q1 = df[col].quantile(0.25)
    IQR = Q3 - Q1
    upper_bound = Q3 + h*IQR
    lower_bound = Q1 - h*IQR
    df_trimmed = df.filter((pl.col(col) >= lower_bound) & (pl.col(col) <= upper_bound))

    return df_trimmed

######################################################################################################################

def quant_to_cat(X, rule, t=0.05, n_intervals=20, random_seed=123, custom_bins=None):

    """
    Parameters (inputs)
    ----------
    X: a polars series or a numpy array (the quantitative variable).
    rule: the name of the categorization rule to be used. The allowed names are 'default', 'mean', 'median', 'quartiles', 'deciles', 'quantiles', 'Scott', 'random'.
    t: a real number between 0 and 1. 
    n_intervals: the number of intervals taken into account when rule='default' or rule='random'.
    intervals: is a boolean, so takes True or False.
               If True, the categorization intervals will be return. If False, not.
    custom_bins: a list with the bins of the custom intervals. Will be used if rule='custom intervals'.
 
    Returns (outputs)
    -------
    X_cat: the categorical version of X.
    intervals: the categorization intervals. Only return if intervals=True.
    """ 
    if isinstance(X, np.ndarray):
        X = pl.Series(X)


    if rule == 'custom_intervals' :

        X_cat = X.cut(breaks=custom_bins)
       
    elif rule == 'mean':  

        X_min = X.min()
        X_max = X.max()
        X_mean = round(X.mean(), 4)
        eps = (X.max() - X.min()) * 0.01
        intervals_limits = [X_min-eps, X_mean, X_max]
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'median':

        X_min = round(X.min(), 3)
        X_max = round(X.max(), 3)
        X_median = round(X.median(), 3)
        eps = (X_max - X_min) * 0.01
        intervals_limits = [X_min - eps, X_median, X_max]
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'quartiles':

        X_min = round(X.min(), 3)
        X_max = round(X.max(), 3)
        Q25 = round(X.quantile(0.25), 3)
        Q50 = round(X.quantile(0.50), 3)
        Q75 = round(X.quantile(0.75), 3)
        eps = (X_max - X_min) * 0.01
        intervals_limits = [X_min - eps, Q25, Q50, Q75, X_max]
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'deciles':

        eps = (X.max() - X.min()) * 0.01
        intervals_limits = []
        for q in np.arange(0, 1.1, step=0.1) :
            Q = round(X.quantile(q), 4)
            intervals_limits.append(Q)
        intervals_limits[0] = intervals_limits[0] - eps
        intervals_limits.append(round(X.quantile(1), 4))
        intervals_limits = list(set(intervals_limits))                        
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'quantiles':
         
        eps = (X.max() - X.min()) * 0.01
        intervals_limits = []
        for q in np.arange(0, 1, step=t) :
            Q = round(X.quantile(q), 4)
            intervals_limits.append(Q)
        intervals_limits[0] = intervals_limits[0] - eps
        intervals_limits.append(round(X.quantile(1), 4))
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'Scott': # A modification of the Scott's rule.

        X_min = X.min()
        X_max = X.max()
        eps = (X.max() - X.min()) * 0.01       

        def scott_intervals(h) :
            w = np.ceil((X_max - X_min)/h)
            L = [None for x in range(h)]
            L[0] = X_min - eps
            for i in range(1, h):
                if L[i-1] < X_max:
                    L[i] = L[0] + i*w
                else:
                    break
            L = np.array(L)
            if np.any(L == None):
                L = list(L)
                L = [x for x in L if x != None]
            if not np.any(np.array(L) >= X_max):
                L = list(L)
                L.append(X_max)                
            return L
        
        intervals_limits = scott_intervals(h=n_intervals)
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    elif rule == 'random':

        X_min = X.min()
        X_max = X.max()
        eps = (X.max() - X.min()) * 0.01       

        def random_intervals(X=X, n_intervals=n_intervals, random_seed=random_seed) :
            random.seed(random_seed)
            L_inner = random.sample(range(int(X_min), int(X_max)+1), n_intervals-1)
            L = [X_min - eps] + L_inner + [X_max]
            L.sort()             
            return L
        
        intervals_limits = random_intervals(X, n_intervals)
        intervals_limits = list(set(intervals_limits))  
        X_cat = X.cut(breaks=intervals_limits)

    
    return X_cat

######################################################################################################################

def transform_to_dummies(X, cols_to_dummies, drop_first=True):

    if isinstance(X, pd.DataFrame):
        X = pl.from_pandas(X)
    elif isinstance(X, np.ndarray):
        X = pl.from_numpy(X)

    for col in cols_to_dummies : 
        if drop_first == True:
            X = X.with_columns(X[[col]].to_dummies()[:,1:])
        else:
            X = X.with_columns(X[[col]].to_dummies())

    X = X[[col for col in X.columns if col not in cols_to_dummies]]

    return X

######################################################################################################################

def count_cols_nulls(X):
    return X.null_count()

######################################################################################################################

def prop_cols_nulls(X):
    num_rows = len(X)
    return  count_cols_nulls(X) / num_rows

######################################################################################################################

def count_row_nulls(X):

    X = X.to_numpy()
    null_count = np.sum(np.isnan(X), axis=1)
    
    if len(X) > 1 :
        return null_count
    elif len(X) == 1:
        return null_count[0]
    
######################################################################################################################

def prop_row_nulls(X) :

    num_columns = X.shape[1]
    return count_row_nulls(X) / num_columns

######################################################################################################################

def all_null_colum(X):
    return count_cols_nulls(X) == len(X)

######################################################################################################################

def too_much_nulls_colums(X, limit):
    return prop_cols_nulls(X) > limit

######################################################################################################################

def null_imputation(df, auto_col=True, quant_col_names=None, cat_col_names=None, quant_method='mean', cat_method='mode', quant_value=None, cat_value=None) :

    """
    Parameters (inputs)
    ----------
    df: a pandas data-frame (the data-matrix).
    quant_method: the name of the method that will be used for quantitative data NaN imputation.
 
    Returns (outputs)
    ----------
    df_new: A pandas data-frame based on df but with all the df missing values filled or imputed.
    """

    df_new = df
    if auto_col == True :
        quant_col_names = columns_names(df=df, types=[pl.Float64, pl.Int64])
        cat_col_names = columns_names(df=df, types=[pl.Boolean, pl.Utf8])
    
    if quant_col_names is not None :

        for col in quant_col_names :

            if quant_method == 'mean' : 
                
               mean = df_new[col].mean()
               df_new = df_new.with_columns(pl.col(col).fill_null(mean))

            elif quant_method == 'median' : 
                
               median = df_new[col].median()
               df_new = df_new.with_columns(pl.col(col).fill_null(median))

            elif quant_method == 'Q25':

               Q25 = df_new[col].quantile(0.25)
               df_new = df_new.with_columns(pl.col(col).fill_null(Q25))            

            elif quant_method == 'Q75':

               Q75 = df_new[col].quantile(0.75)
               df_new = df_new.with_columns(pl.col(col).fill_null(Q75))  

            elif quant_method == 'max':

               max = df_new[col].max()
               df_new = df_new.with_columns(pl.col(col).fill_null(max)) 

            elif quant_method == 'min':

               min = df_new[col].min()
               df_new = df_new.with_columns(pl.col(col).fill_null(min)) 

            elif quant_method == 'free':

               df_new = df_new.with_columns(pl.col(col).fill_null(quant_value))

    if cat_col_names is not None :
        
        for col in cat_col_names :
            
            if cat_method == 'mode':
            
               mode = df_new[col].mode()
               df_new = df_new.with_columns(pl.col(col).fill_null(mode))

            elif cat_method == 'free':

               df_new = df_new.with_columns(pl.col(col).fill_null(cat_value))

    return df_new
    
######################################################################################################################
