import sys


def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


# Which one of the log entry fields can be used as a key?
# IP address, resource path
# How do you store the remaining data of each entry?
# Tuple
def read_log():
    log_dict = dict()
    file_content = read_file("access_log-20201025.txt")
    print(file_content)
    return log_dict


def run():
    entries = read_log()


if __name__ == "__main__":
    run()
