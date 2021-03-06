import sys
from collections import defaultdict


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


# Which one of the log entry fields can be used as a key?
# IP address, resource path, date. I used the former
# How do you store the remaining data of each entry?
# String
def read_log():
    # dictionary values are empty lists by default
    log_dict = defaultdict(list)

    file_content = read_file("access_log-20201025.txt")
    lines = file_content.split('\n')

    for rawLine in lines:
        # check if line not empty
        if rawLine:
            ip_address = rawLine.split(" - - ")[0]
            log_entry = rawLine.split(" - - ")[1]
            log_dict[ip_address].append(log_entry)

    return log_dict


# 3)
def run():
    # 4)
    log_dict = read_log()
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
