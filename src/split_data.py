import os
import argparse
import pandas
from sklearn.model_selection import train_test_split
from get_data import read_config


def split_data(params):
    test_data_path = params["split_data"]["test_path"]
    train_data_path = params["split_data"]["train_path"]
    raw_data_path = params["load_data"]["raw_dataset_csv"]
    split_ratio = params["split_data"]["test_size"]
    random_state = params["base"]["random_state"]

    data_frame = pandas.read_csv(raw_data_path, sep=",")
    train, test = train_test_split(data_frame, test_size=split_ratio, random_state=random_state)
    train.to_csv(train_data_path, sep=",", index=False, encoding="utf-8")
    test.to_csv(test_data_path, sep=",", index=False, encoding="utf-8")


def main(args):
    params = read_config(args.config)
    split_data(params)

def args_parser():
    args = argparse.ArgumentParser()
    args.add_argument("--config", help="Pass the config file")
    return args.parse_args()

if __name__ == "__main__":
    main(args_parser())

