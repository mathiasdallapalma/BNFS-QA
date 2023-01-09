# import exact_solver, dwave_solver
from utils import common
from bnfsqa.discretize import discretize
from bnfsqa.bnsl import bnsl
from bnfsqa.markov_blanket import markov_blanket

import argparse
import json
import sys
import logging as log


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--config_file", required=True, type=str)
    args = parser.parse_args()

    config, df, df_disc = common.load_config_and_input_data(args.config_file)

    if config["verbose"]:
        log.getLogger().setLevel(log.INFO)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")

    log.getLogger().setLevel(log.DEBUG)

    if config["discretize"]:
        df_disc = discretize.main(config, df)

    bn = bnsl.main(config, df_disc)
    log.info(bn)
    features = markov_blanket.main(config, bn)
    print(features)


if __name__ == '__main__':
    main()
