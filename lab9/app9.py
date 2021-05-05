import argparse
import json
import sys

import bs4
import requests
from json import JSONDecodeError

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mail")
parser.add_argument("-c", "--cat-facts", type=int)
parser.add_argument("-t", "--teachers")


def read_config():
    try:
        with open('private.json') as f:
            config_dict = json.load(f)
            return config_dict
    except FileNotFoundError:
        print('Error: Config file not found.')
        sys.exit(0)
    except JSONDecodeError:
        print('Error: Invalid JSON.')
        sys.exit(0)


def send_mail(mail_message, config):
    pass


def print_cat_facts(count):
    r = requests.get(f'https://cat-fact.herokuapp.com/facts/random?amount={count}')

    if r.status_code == 200:
        print(f"{count} cat facts:")
        for x in r.json():
            print(f"{x.get('text')}")
    pass


def print_teachers(prefix):
    r = requests.get(f'https://wiz.pwr.edu.pl/pracownicy?letter={prefix}')
    r.raise_for_status()

    content = bs4.BeautifulSoup(r.text, 'html.parser')

    print(f"The list of researchers - {prefix}")
    people_tiles = content.select('.column-content .news-box .col-text.text-content')

    if len(people_tiles) == 0:
        print("<no results>")

    for person in people_tiles:
        name = person.select("a.title")[0].text
        email = person.select("p")[0].text
        print(f"{name} ({email})")

    pass


def run():
    args = parser.parse_args()
    config = read_config()

    mail_message = args.mail
    if mail_message:
        send_mail(mail_message, config)

    cat_facts_count = args.cat_facts
    if cat_facts_count:
        print_cat_facts(cat_facts_count)

    teacher_last_name_prefix = args.teachers
    if teacher_last_name_prefix:
        print_teachers(teacher_last_name_prefix)


if __name__ == "__main__":
    run()
