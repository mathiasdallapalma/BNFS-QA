import logging as log
import os
from utils import common
import pandas as pd
import subprocess
from pathlib import Path
def main(config,df):
    """Learn the bayesian network strutcture of the input dataset
    Parameters
    ----------
    config: dictionary
        Contains all the parameters for this phase.
    Returns
    -------
    pd.DataFrame
        DAG of Bayesian network. #TODO guarda
    """
    output_dir = config["output_dir"]
    strategy=config["strategy"]

    if config["divide_et_impera"]:
        if strategy!="QA":
            log.error("Divide et Impera approach can be used only with QA strategy.")
            exit(1)

        files=divide_et_impera(config,df)
        for file in files:
            command="cd ./BNSL-QA-python; python3 -m bnslqa solve "+path+"/"+file+" QA -r 1000"

            result = subprocess.check_output(command, shell=True)

            #reconstruct(fs)
        
        print(files)

    else:
        if config["discretize"]:
            file=config["output_dir"]+"/"+config["data_path"].split('.')[0]+'_'+str(config["n_bins"])+"b.txt"
        else:
            file=config["bnsl_data_path"]

    if strategy=="QA" or strategy=="SA" :
        print("QA")
        command="cd ./BNSL-QA-python; python3 -m bnslqa solve %s %s -r %d -a %d"%(file,strategy,config["QA_kwargs"]["reads"],config["QA_kwargs"]["annealing_time"])

        #result = subprocess.check_output(command, shell=True)
        #print(result)
        bn=get_solution(1) #TODO prendere soluzione da result

    elif strategy=="bnlearn":
        print("bn")
         
    else:
        log.error("Unknown strategy, please choose between [QA,SA,bnlearn].")
        exit(1)
        
    #return

def divide_et_impera(config,df):    
    """Divide the discretized dataset in order to be executed by qa
    Parameters
    ----------
    config: dictionary
        Contains all the parameters for this phase.
    df: pd.DataFrame
        Dataframe of the discretized dataset
    Returns
    -------
    files: list of str
        #TODO
    """

    n = int(config["dei_n"])
    if n<3 or n>9:
        log.error("dei_n must be between 3 and 9 (included).")
        exit(1)

    mod=(len(df.columns)-1)%n
    print("%d,%d,%d"%(len(df.columns),mod,n))
    if mod<2 and mod!=0:
        log.error("Last group will be combosed by %d features, wich is impossible to solve."%mod)
        exit(1)
    elif mod/2<n and mod!=0:
        log.warn("Last group will be combosed by %d features. (Other group are composed by %d features)"%(mod,n))

    dataset_name=config["data_path"].split('.')[0]
    dir=config["output_dir"]+"/divided/"+dataset_name
    if not os.path.exists(dir):
        os.makedirs(dir)

    actual=0
    next=n
    i=0
    files=[]

    while next<len(df.columns):
        df1=pd.concat([df.iloc[:, actual:next],df.iloc[:,-1:]], axis=1)
        print(df1)

        common.save_txt(df1,"{}_{}".format(dataset_name,i),"{}/{}.txt".format(dir,i))
        files+=["divided/{}/{}_{}.txt".format(dataset_name,dataset_name,i)]

        actual=next
        next+=n
        i+=1
    
    df1=df.iloc[:, actual:len(df.columns)]
    print(df1)

    common.save_txt(df1,"{}_{}".format(dataset_name,i),"{}/{}.txt".format(dir,i))
    files+=["divided/{}/{}_{}.txt".format(dataset_name,dataset_name,i)]

    return files



        
