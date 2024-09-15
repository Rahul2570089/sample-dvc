import os
import yaml
import argparse
import pandas


def get_data(params):
    data_path = params["data_source"]["s3_source"]
    data_frame = pandas.read_csv(data_path, sep=",", encoding="utf-8")
    return data_frame

def read_config(config):
    with open(config, "r") as yaml_file:
        params = yaml.safe_load(yaml_file)
    return params

def main(args):
    params = read_config(args.config)
    get_data(params)

def args_parser():
    args = argparse.ArgumentParser()
    args.add_argument("--config", help="Pass the config file")
    return args.parse_args()

if __name__ == "__main__":
    main(args_parser())