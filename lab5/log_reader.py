import json
import re
import sys
import logging
from collections import defaultdict
from json import JSONDecodeError
from typing import List


logger = logging.getLogger('lab5')
ch = logging.StreamHandler()
logger.addHandler(ch)


def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


def flatten(nested_list: list):
    return [item for sublist in nested_list for item in sublist]


def get_request_string(log_line: str):
    start, end = '] ', '" '

    a, b = log_line.find(start), log_line.find(end)
    # returns the text between 'start' and 'end'
    return log_line[a + len(start) + 1:b]


def longest_request(log_dict: dict):
    log_lines = list()

    for k, v in log_dict.items():
        for entry in v:
            log_lines.append((k, entry))

    ordered = sorted(log_lines, key=lambda x: len(get_request_string(x[1])), reverse=True)

    return ordered[0]


def get_status_code(log_line: str):
    return int(log_line.split("\" ")[1].split(" ")[0])


def non_existent(log_dict: dict):
    non_existent_resources = set()

    for k, v in log_dict.items():
        for entry in v:
            if get_status_code(entry) == 404:
                non_existent_resources.add(get_request_string(entry))

    return non_existent_resources


def ip_find(ip_requests_number_dict, most_active=True):
    target = max(ip_requests_number_dict.values()) if most_active \
        else min(ip_requests_number_dict.values())

    return [k for k, v in ip_requests_number_dict.items() if v == target]


def ip_requests_number(log_dict: dict):
    new_dict = dict()

    for k, v in log_dict.items():
        new_dict[k] = len(v)

    return new_dict


def read_log(log_path: str):
    # dictionary values are empty lists by default
    log_dict = defaultdict(list)

    try:
        file_content = read_file(log_path)
        lines = file_content.split('\n')

        for rawLine in lines:
            # check if line not empty
            if rawLine:
                ip_address = rawLine.split(" - - ")[0]
                log_entry = rawLine.split(" - - ")[1]
                log_dict[ip_address].append(log_entry)

        return log_dict
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


def read_config(required_fields: List[str]):
    try:
        with open('config.json') as f:
            config_dict = json.load(f)

            differences = list(set(required_fields) - set(config_dict.keys()))
            if differences:
                raise ValueError(f"Error: Missing configuration keys: {', '.join(differences)}.")

            return config_dict
    except FileNotFoundError:
        print('Error: Config file not found.')
        sys.exit(0)
    except JSONDecodeError:
        print('Error: Invalid JSON.')
        sys.exit(0)
    except ValueError as e:
        print(e)
        sys.exit(0)


def print_welcome_message(message: str):
    print(message)


def set_logging_level(logging_level: str):
    def logging_to_number(x):
        return {
            'CRITICAL': 50,
            'ERROR': 40,
            'WARNING': 30,
            'INFO': 20,
            'DEBUG': 10,
        }.get(x, 0)  # 0 is default log level (NOTSET)

    converted_logging_level = logging_to_number(logging_level)

    logger.setLevel(converted_logging_level)
    ch.setLevel(converted_logging_level)


def print_all_index_requests(log_dict: dict):
    all_requests = set()

    expected_path = "/index.html"

    for k, v in log_dict.items():
        for entry in v:
            all_requests.add(get_request_string(entry))

    for request_string in all_requests:
        try:
            METHOD = 0
            PATH = 1

            request = request_string.split(" ")
            request_method = request[METHOD]
            request_path = request[PATH]

            if request_path == expected_path:
                print(f"{request_method} {request_path}")
        except:
            pass


def run():
    required_fields = ["log_file_name", "http_request_method", "logging_level", "log_page_size", "welcome_text"]

    config = read_config(required_fields)

    print_welcome_message(config.get("welcome_text"))
    set_logging_level(config.get("logging_level"))


    log_dict = read_log(config.get("log_file_name"))
    ### lab5 code below ###
    # 4)
    print(print_all_index_requests(log_dict))

    ### lab4 code below ###
    # print(log_dict)

    # 5)
    # keeps number of requests per ip address
    # ip_requests_number_dict = ip_requests_number(log_dict)
    # print(ip_requests_number_dict)

    # 6)
    # most active IP addresses
    # print(ip_find(ip_requests_number_dict))
    # least active IP addresses
    # print(ip_find(ip_requests_number_dict, most_active=False))

    # 7)
    # print(longest_request(log_dict))

    # 8)
    # print(list(non_existent(log_dict)))


if __name__ == "__main__":
    run()
