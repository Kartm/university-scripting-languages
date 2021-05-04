import csv
import argparse
import sys

# https://www.kaggle.com/rdoume/beerreviews
from collections import defaultdict
from typing import List

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
    def __init__(self, brewery_name, review_overall, review_profilename, beer_style):
        self.brewery_name = brewery_name
        self.review_overall = review_overall
        self.review_profilename = review_profilename
        self.beer_style = beer_style

    def __str__(self):
        return f"{self.brewery_name}'s {self.beer_style} was rated {self.review_overall} by {self.review_profilename}"

    def __repr__(self):
        return f"{self.brewery_name}'s {self.beer_style} was rated {self.review_overall} by {self.review_profilename}"


def read_csv_file(path: str):
    i = 0

    rows = []
    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # skip header

        for row in reader:
            rows.append(BeerReview(brewery_name=row[1],
                                   review_overall=float(row[3]),
                                   review_profilename=row[6],
                                   beer_style=row[7]
                                   ))

            i += 1
            if i == 100:
                break

    return rows


def read_dataset(path: str):
    try:
        return read_csv_file(path)
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


def print_stats(reviews: List[BeerReview]):
    mean_rating = sum(review.review_overall for review in reviews)/len(reviews)
    print(f"Mean rating: {mean_rating}\n")

    # worst rating by profile
    worst_ratings_of_users = dict()
    for review in reviews:
        if worst_ratings_of_users.get(review.review_profilename):
            worst_ratings_of_users[review.review_profilename] = min(
                review.review_overall,
                worst_ratings_of_users.get(review.review_profilename)
            )
        else:
            worst_ratings_of_users[review.review_profilename] = review.review_overall

    print(f"Worst ratings of users: {worst_ratings_of_users}\n")

    print(f"All reviews: {len(reviews)}\n")

def run():
    dataset_path = get_dataset_path()
    dataset = read_dataset(dataset_path)
    print_stats(dataset)
    # print(dataset)


if __name__ == "__main__":
    run()
