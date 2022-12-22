import sys
import json
import pandas as pd
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

