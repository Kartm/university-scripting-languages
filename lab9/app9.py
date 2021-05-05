import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mail")
parser.add_argument("-c", "--cat-facts")
parser.add_argument("-t", "--teachers")


def send_mail(mail_message):
    pass


def print_cat_facts(cat_facts):
    pass


def print_teachers(teacher_last_name_prefix):
    pass


def run():
    args = parser.parse_args()

    mail_message = args.mail
    if mail_message:
        send_mail(mail_message)

    cat_facts = args.cat_facts
    if cat_facts:
        print_cat_facts(cat_facts)

    teacher_last_name_prefix = args.teachers
    if teacher_last_name_prefix:
        print_teachers(teacher_last_name_prefix)


if __name__ == "__main__":
    run()
