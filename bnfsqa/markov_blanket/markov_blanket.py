import numpy as np
def main(config,bn):
    """Selected most relevant features using markov blanket of the Bayesian Network
    Parameters
    ----------
    config: dictionary
        Contains all the parameters for this phase.
    bn: np.ndarray
        Bayesian Network adjency matrix
    Returns
    -------
    list
        Features selected using markov blanket of the bayesian network
    """
    
    last_row=bn[-1,:-1]
    last_col=bn[:-1,-1]

    features=last_row+last_col

    if config["full_Markov_blanket"]:
        i=0
        sons=np.zeros(len(bn)-1)
        
        for b in last_row:
            if b:
                x=bn[:-1,i]
                sons+=x
            i+=1
        
        sons=sons.astype(int)
        
        features+=sons
        features[features>1]=1

    return features