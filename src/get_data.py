import os
import yaml
import argparse
import pandas


def get_data(config_path):
    with open(config_path, "r") as yaml_file:
        params = yaml.safe_load(yaml_file)
    data_path = params["data_source"]["s3_source"]
    data_frame = pandas.read_csv(data_path, sep=",", encoding="utf-8")
    return data_frame

def main(args):
    get_data(args.config)

def args_parser():
    args = argparse.ArgumentParser()
    args.add_argument("--config", help="Pass the config file")
    return args.parse_args()

if __name__ == "__main__":
    main(args_parser())