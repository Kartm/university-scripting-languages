import argparse
import json
import sys
import smtplib
from datetime import datetime

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
    smtpSrv = smtplib.SMTP('smtp.gmail.com', 587)

    smtpSrv.starttls()
    print("Logging in...")
    login = config.get('mail_login')
    password = config.get('mail_password')
    login_status = smtpSrv.login(login, password)
    print(f"Logged in. {login_status}")

    sender = login
    to = 'bogumila.hnatkowska@pwr.edu.pl'

    subject = f"Hello! {datetime.now().strftime('%H:%M:%S, %d/%m/%Y')}"
    header = 'To:' + to + '\n' + 'From: ' + sender + '\n';
    message = f'{header}Subject: {subject}\n{mail_message}'

    result = smtpSrv.sendmail(sender, to, message)
    print(f"Errors: {result}")
    smtpSrv.quit()

    pass


def print_cat_facts(count):
    r = requests.get(f'https://cat-fact.herokuapp.com/facts/random?amount={count}')

    if r.status_code == 200:
        print(f"{count} cat facts:")
        response = r.json()

        if type(response) == list:
            for x in r.json():
                print(f"{x.get('text')}")
        elif type(response) == dict:
            print(f"{response.get('text')}")
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
