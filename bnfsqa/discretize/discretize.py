import logging as log
from sklearn import preprocessing
import pandas as pd
import numpy as np
from utils import common

def main(config,df):
    """Discretize the input dataset
    Parameters
    ----------
    config: dictionary
        Contains all the parameters for this phase.
    df : pd.DataFrame
        Original dataframe of the dataset.
    Returns
    -------
    pd.DataFrame
        Discretized dataset.
    """

    dataset_path = config["data_path"]
    output_dir = config["output_dir"]
    labels = list(map(int, config["labels"].split(',')))
    n_bins = int(config["n_bins"])
    discretizer_strategy = config["discretizer_strategy"]
    keep_file =  bool(config["keep_file"])

    df_disc=discretize(df,labels,n_bins,discretizer_strategy)


    dataset_name=dataset_path.split('.')[0]
    output_path=output_dir+'/'+dataset_name+'_'+str(n_bins)+"b.txt"
    
    common.save_txt(df_disc,dataset_name,output_path)

    if(keep_file):
        save_csv(df_disc,dataset_name,output_dir,n_bins)
        
    
    return df_disc

def discretize(df,labels,n_bins,discretizer_strategy):
    """Discretize the input dataframe and check for possible errors (throw wornings)
    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe of the dataset.
    labels: list
        Indexes of the categorical features in the dataset
    n_bins : int
        Number of bins
    discretizer_strategy : str
        ['uniform, 'quantile', 'kmeans']
    random_state : int
    
    Returns
    -------
    pd.DataFrame
        Discretized dataset.
    """

    global categorical_columns,numerical_columns

    columns=df.columns
    categorical_columns=[columns[i] for i in labels]
    numerical_columns=list(set(columns)-set(categorical_columns))

    df[categorical_columns]=df[categorical_columns].apply(preprocessing.LabelEncoder().fit_transform)
    
    discretizer=preprocessing.KBinsDiscretizer(n_bins=n_bins, encode='ordinal', strategy=discretizer_strategy)
    df[numerical_columns]=pd.DataFrame(discretizer.fit_transform(df[numerical_columns]), columns = numerical_columns, dtype=int) #funziona

    log.info("Discretization completed")

    check_for_errors(df,n_bins)
    
    return df 

def save_csv(df_disc,dataset_name,output_dir,n_bins,):
    """Save the discretize dataframe in a new csv file
    Parameters
    ----------
    df_disc : pd.DataFrame
        Discretized dataframe of the dataset.
    dataset_path: str
        Path of the original dataset
    output_dir:str
        Path where save the new discretized dataset
    n_bins : int
        Number of bins

    Returns
    -------
    None
    """

    output_path=output_dir+'/'+dataset_name+'_'+str(n_bins)+"b.csv"
    df_disc.to_csv(output_path,index=False)
    log.info("Discretized dataset saved in : "+output_path)

def check_for_errors(df_disc,n_bins):
    """Check the discretized dataframe for errors
    Parameters
    ----------
    df_disc: pd.DataFrame
        Discretized dataframe of the dataset.
    n_bins : int
        Number of bins

    Returns
    -------
    None
    """

    for feature in df_disc[numerical_columns]:
        n = len(pd.unique(df_disc[feature]))
        if(n<n_bins):
            log.warn("number of unique values in feature: \"%s\" after disctetization is %d.(number of bins is %d)\n Usually that means there are some outliers values."%(feature,n,n_bins))
    
    for feature in df_disc[categorical_columns]:
        n = len(pd.unique(df_disc[feature]))
        if(n>n_bins):
            log.warn("number of unique values in feature: \"%s\" after disctetization is %d.(number of bins is %d)\n That maight be too hight, please consider another type of categorical encoding."%(feature,n,n_bins))

    