import os
import argparse
import pandas
from get_data import get_data, read_config


def load_data(params):
    data_frame = get_data(params)
    cols = [col.replace(' ', '_') for col in data_frame.columns]
    raw_data_path = params["load_data"]["raw_dataset_csv"]
    data_frame.to_csv(raw_data_path, sep=",", index=False, header=cols)


def main(args):
    params = read_config(args.config)
    load_data(params)

def args_parser():
    args = argparse.ArgumentParser()
    args.add_argument("--config", help="Pass the config file")
    return args.parse_args()

if __name__ == "__main__":
    main(args_parser())