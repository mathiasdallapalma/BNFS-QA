# Baesyan Network Feature Selection
Feature selection for classification and regression. 

Final application project at Trento University

## Table of Contents  
[Introduction](#introduction)  
[Installation](#installation)  
[Running BNFS](#running-bnsl)  


# Introduction

<img align="right" width="400px" src="">
<div>
<p>Bayesian Network Feature Selection (BNFS) implements a way to solve the problem of feature selection using the Bayesian Networks.
Bayesian networks can be used to model relationships between variables in a dataset and estimate the strength of these relationships through probabilities. These probabilities can then be used as a measure of the importance of the features in the dataset and therefore select the most important features for the prediction problem.

Briefly, a pipeline is implemented as follows:
</p>
<ol>
  <li><i>Preprocess the data:</i> clean and normalize the data to ensure that it is in a format that can be used to train a Bayesian network. This step also include the discretization of the data.</li>
  <li><i>Bayesian Network Structure Learning:</i> Decide which variables should be included as nodes in the network and how they should be connected. </li>
  <li><i>Markov blanket:</i> determines the Markov blanket of the target feature.</li>
  <li><i>Feature Selection:</i> selects the features from the Markov blanket that are most relevant for predicting the target feature.</li>
</ol>
</div>

# Installation

### Prerequisites:
Make sure you have installed all of the following prerequisites on your development machine:
  - python3.6+  
  - pip3


### BNFS installation:  
`pip3 install bnfs`

# Running BNFS

## Step 1: data preparation

Before running the tool, you should prepare the csv table containing the actual sample and The target variable(the variable whose values are modeled and predicted by other variables):

<details>
  <summary>Example</summary>
  
| Feature 1 | Feature 2 | Feature 3 | TARGET    |
| --------- | --------- | --------- | --------- |
| 17.27     | 3         | ETVDA     | True      |
| 44.59     | 105       | FBAER     | False     |
| ...       | ...       | ...       | ...       |
| 26.89     | 19        | DDFBDF    | False     |
| 15.56     | 298       | CSDSD     | True      |
</details>

Please note that the type of each feature column could be any kind (integer, float, string) and that the TARGET value is the last column of the dataframe. 

## Step 2: creating configuration file

Configuration file is a json file containing all customizable parameters for the feature selection algorithm.  

<details>
  <summary>Available parameters</summary> 

  🔴!NOTE! - All paths to files / directories can be either relative to the configuration file directory or absolute paths 
  * `data_path`
      Path to csv table of the data.

  * `output_dir`
      Path to directory for output files. If it doesn't exist, it will be created.
  
  * `random_state`
      Random seed (set to an arbitrary integer for reproducibility).

  * `verbose`
      If *true*, print info messages at each step (discretization,bnlearn and markov blanket search).

  * `full_Markov_blanket`
      If *true*, the feature selected will be the union of the nodes parent, children and the children's parent, otherwise only parent and children.

<h2>Discretization</h2>

  * `discretize`
      If *flase* skips the discretization steps.

  * `labels`
      List of index position of the feature that are categorical and therfore need a label encoding.

  * `n_bins`
      Number of bins for discretization.
  
  * `discretizer_strategy`
      Strategy used to define the widths of the bins.
      {‘uniform’, ‘quantile’, ‘kmeans’}

  * `keep_file`
      If *true* generates a csv file with the discretized dataset.
  
  * `divide_et_impera`
      If *true* ecxecute the steps for the divide et impera approach.

<h2>Bayesian Network Structure Learning</h2>

  * `dei_n`
      Number of splits for the divide et impera approach.

  * `bnsl_data_path`
       Path to csv table of the discretized data. (Used when discretization step is skipped)

  * `bnsl_strategy`
       Strategy used to learn the structure of the Bayesian network from data.
       {QA, SA, bnlearn}

<h3>QA_kwargs</h3> 

  * `reads`
    Number of reads for the annealing method

  * `annealing_time`
    Time in microseconds of quantum annealing time per read

<h3>bnlearn_kwargs</h3> 

  * `metric`
    The scoring function indicates how well the Bayesian network fits the data.
    {k2, bic, bdeu}

  * `search_algorithm`
    The search algorithm to optimize throughout the search space of all possible DAGs.
    {ex, hc, cl, tan, cs, naivebayes}

 
</details>

## Step 4: running the pipeline

When input data and configuration file are ready,  
the algorithm can be executed as follows -  

```bash
bnfs -c <config_file>
```

This will generate multiple info messages in the console and a summary file in the specified output folder:
* `res.txt`: this file contains the structure as adjency matrix of the Bayesian network learned and a list of feature selected using the Markov blanket method.
