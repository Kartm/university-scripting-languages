import csv
import argparse
import sys

# https://www.kaggle.com/rdoume/beerreviews

parser = argparse.ArgumentParser()
parser.add_argument(
    "path",
    help="dataset path",
)


def get_dataset_path():
    args = parser.parse_args()

    path = args.path
    if len(path) > 1:
        if path.endswith(".csv"):
            return path
        print("Dataset path must end with \".csv\".")
        sys.exit(0)
    print("Dataset path must be specified.")
    sys.exit(0)


class BeerReview:
    def __init__(self, brewery_name):
        self.brewery_name = brewery_name

    def __str__(self):
        return f"{self.brewery_name}"

    def __repr__(self):
        return f"{self.brewery_name}"


def read_csv_file(path: str):
    i = 0

    rows = []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            print(row[1])
            rows.append(BeerReview(brewery_name=row[1]))

            i += 1
            if i == 10:
                break

    return rows


def read_dataset(path: str):
    try:
        return read_csv_file(path)
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


def run():
    dataset_path = get_dataset_path()
    dataset = read_dataset(dataset_path)
    # print(dataset)


if __name__ == "__main__":
    run()
