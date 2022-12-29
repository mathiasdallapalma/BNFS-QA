import sys
import json
import pandas as pd
import numpy as np
import os
import logging as log
def load_config_and_input_data(config_path):

    """Load configuration file and input data
    Parameters
    ----------
    config_path : string
        Path to config file (json).
    Returns
    -------
    dict, pd.DataFrame
        Dict with configuration, data (df)
    """

    log.info('Loading data...')
    try:
        config_file = open(config_path, 'r')
    except:
        log.error('Cannot open configuration file', file=sys.stderr)
        sys.exit(1)

    try:
        config = json.load(config_file)
    except:
        log.error('Please specify valid json configuration file', file=sys.stderr)
        sys.exit(1)

    config_dirname = os.path.dirname(config_path)
    df = pd.read_csv(os.path.join(config_dirname, config['data_path']).replace('\\','/'), index_col=None)

    if not os.path.exists(config["output_dir"]):     
        os.makedirs(config["output_dir"])

    return config,df

def save_txt(df_disc,dataset_name,output_path):
    """Save the discretize dataframe in a new txt file, used as input for bnslqa
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

    file_out = open(output_path, 'w')

    lenM=len(df_disc.columns)
    sol=np.zeros(lenM*(lenM-1),dtype=int)
        
    feature_cardinality=[]

    for feature in df_disc:
        feature_cardinality+=[len(pd.unique(df_disc[feature]))]  

    file_out.write("{} {}\n".format(lenM," ".join(map(str, feature_cardinality))))
    file_out.write("{}\n".format(dataset_name))
    file_out.write("{}\n".format(" ".join(map(str, sol))))

    np.savetxt(file_out, df_disc, fmt="%.0f")
    file_out.close()

    log.info("File saved in : "+output_path)
    

