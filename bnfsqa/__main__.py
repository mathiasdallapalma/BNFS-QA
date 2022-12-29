#import exact_solver, dwave_solver
from utils import common 
from bnfsqa.discretize import discretize
from bnfsqa.bnsl import bnsl


import argparse
import json
import sys
import logging as log

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--config_file", required=True, type=str)
    args = parser.parse_args()
    

    config,df = common.load_config_and_input_data(args.config_file)
    
    if config["verbose"]:
        log.getLogger().setLevel(log.INFO)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    if not config["skip_discretization"]:
        disc_df=discretize.main(config,df)

    bn=bnsl.main(config,disc_df)




        


if __name__ == '__main__':
  main()


  
  

