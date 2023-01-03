import logging as log
import pandas as pd
import numpy as np
import scipy
import bnlearn 
import torch
import os

import sys
bnslqa_path = os.path.join(os.getcwd(),"BNSL-QA-python")
sys.path.insert(0, bnslqa_path)

from bnslqa.solvers.qubo_matrix import calcQUBOMatrix                                        
from bnslqa.solvers.dwave_solver import dwaveSolve


def main(config,df):
    """Learn the bayesian network strutcture of the input dataset
    Parameters
    ----------
    config: dictionary
        Contains all the parameters for this phase.
    Returns
    -------
    bn: np.ndarray
        Final Bayesian Network adjency matrix
    """

    strategy=config["strategy"]

    if config["divide_et_impera"]:
        
        if strategy!="QA":
            log.error("Divide et Impera approach can be used only with QA strategy.")
            exit(1)
        

        dfs=divide_et_impera(config,df) 
        bns=[]
        for df_i in dfs:
            examples=df_i.values.tolist()
            states=[]

            for feature in df_i:
                states+=[len(pd.unique(df_i[feature]))]  
            bns+=[bnsl_qa(examples, len(df_i.columns), states,strategy,config["QA_kwargs"]["reads"],config["QA_kwargs"]["annealing_time"])]

        bn=reconstruct(bns)

    elif strategy=="QA" or strategy=="SA" :
        examples=df.values.tolist()
        states=[]

        for feature in df:
            states+=[len(pd.unique(df[feature]))]  

        bn=bnsl_qa(examples, len(df.columns), states,strategy,config["QA_kwargs"]["reads"],config["QA_kwargs"]["annealing_time"])
    
    elif strategy=="bnlearn":
        log.info("Retrieving BN structure using bnlearn library")
        model = bnlearn.structure_learning.fit(df, methodtype=config["bnlearn_kwagrs"]["search_algorithm"], scoretype=config["bnlearn_kwagrs"]["metric"])
        bn= model['adjmat']
        bn= bn.astype(int).to_numpy()

    else:
        log.error("Unknown strategy, please choose between [QA,SA,bnlearn].")
        exit(1)
        
    return bn

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

    actual=0
    next=n
    i=0
    dfs=[]

    while next<len(df.columns):
        dfs+=[pd.concat([df.iloc[:, actual:next],df.iloc[:,-1:]], axis=1)]

        actual=next
        next+=n
        i+=1
    
    dfs+=[df.iloc[:, actual:len(df.columns)]]

    return dfs 

def reconstruct(bns):
    """Reconstruct the complessive solution by joining the divided ones
    Parameters
    ----------
    bns: list of numpy.ndarray
        Array of partial Bayesian Network matrix
    Returns
    -------
    bn: np.ndarray
        Final Bayesian Network matrix
    """
    last_row=[]
    last_col=[]
    bn_0=bns[0]
    sol=bn_0[:-1,:-1]
    i=0
    for bn_i in bns:
        if(i!=0):
            sol=scipy.linalg.block_diag(sol, bn_i[:-1,:-1])
        last_row=np.append(last_row,bn_i[-1,:-1])
        for r in bn_i[:-1]:
            last_col+=[r[-1]]
        i+=1
            
    last_col+=[0]

    sol = np.vstack([sol, last_row])
    sol = np.column_stack((sol, last_col))

    return sol

def bnsl_qa(examples, n, states,method,nReads,annealTime):
    """Estimates the Bayesian Network's structure using annealing 
    Parameters
    ----------
    examples: list of lists
        Dataframe of the dataset
    n : int
        Number of variables
    states : list of int
        Number of states for each variables
    method : str {QA,SA}
        Approach used to estimate the structure
    nReads : int
        Indicates the number of states (output solutions) to read from the solver
    annealTime : int
        Sets the duration of quantum annealing time, per read
    Returns
    -------
    bn: np.ndarray
        Final Bayesian Network adjency matrix
    """

    #calculate the QUBO matrix given the dataset path
    alpha = '1/(ri*qi)'
    log.info("Calculating the QUBO matrix")
    Q, indexQUBO, posOfIndex = calcQUBOMatrix(examples,n,states,alpha=alpha)
    Q = torch.tensor(Q)

    #find minimum of the QUBO problem xt Q x using the specified sampler
    label=""
    log.info("Retrieving BN structure using annealing method")
    minXt,minY,readFound,occurrences,annealTimeRes = dwaveSolve(Q,indexQUBO,posOfIndex,label,method=method,nReads=nReads,annealTime=annealTime)

    narcs = n*(n-1)
    bn= torch.cat([torch.cat([torch.zeros(n-1).view(-1,1),minXt[:narcs].view(-1,n)],dim=-1).view(-1),torch.zeros(1)]).view(n,n).int()
    bn=bn.numpy()
    return bn




        
