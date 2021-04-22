import csv
import sys


# https://www.kaggle.com/rdoume/beerreviews
def get_dataset_path():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if path.endswith(".csv"):
            return path
        print("Dataset path must end with \".csv\".")
        sys.exit(0)
    print("Dataset path must be specified.")
    sys.exit(0)


def read_csv_file(path: str):
    with open(path) as f:
        return csv.reader(f, delimiter=' ', quotechar='|')


def read_dataset(path: str):
    try:
        return read_csv_file(path)
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


def run():
    dataset_path = get_dataset_path()
    dataset = read_dataset(dataset_path)
    print(dataset)


if __name__ == "__main__":
    run()
