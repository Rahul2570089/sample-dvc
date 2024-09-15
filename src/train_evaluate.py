import os
import argparse
import joblib
import json
import pandas
import numpy
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from get_data import read_config


def eval_metrics(actual, pred):
    rmse = numpy.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2
    


def train_evaluate(params):
    test_data_path = params["split_data"]["test_path"]
    train_data_path = params["split_data"]["train_path"]
    random_state = params["base"]["random_state"]
    model_dir = params["model_dir"]

    alpha = params["estimators"]["ElasticNet"]["params"]["alpha"]
    l1_ratio = params["estimators"]["ElasticNet"]["params"]["l1_ratio"]
    target = params["base"]["target_col"]
    train = pandas.read_csv(train_data_path, sep=",")
    test = pandas.read_csv(test_data_path, sep=",")
    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)
    
    lr = ElasticNet(
        alpha=alpha,
        l1_ratio=l1_ratio,
        random_state=random_state
    )
    lr.fit(train_x, train_y)

    predicted_qualities = lr.predict(test_x)
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)
    
    scores_file = params["reports"]["scores"]
    params_file = params["reports"]["params"]
    
    with open(scores_file, "w") as f:
        scores = {
            "rmse": rmse,
            "mae": mae,
            "r2": r2
        }
        json.dump(scores, f, indent=4)
    
    with open(params_file, "w") as f:
        params = {
            "alpha": alpha,
            "l1_ratio": l1_ratio
        }
        json.dump(params, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(lr, model_path)


def main(args):
    params = read_config(args.config)
    train_evaluate(params)

def args_parser():
    args = argparse.ArgumentParser()
    args.add_argument("--config", help="Pass the config file")
    return args.parse_args()

if __name__ == "__main__":
    main(args_parser())
