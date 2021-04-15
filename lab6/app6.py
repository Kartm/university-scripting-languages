import datetime
import re
import sys
import logging
from time import strptime
from typing import List

logger = logging.getLogger('lab5')
ch = logging.StreamHandler()
logger.addHandler(ch)

defaults = {
    'log_file_name': 'access_log-20201025.txt',
    'logging_level_str': 'DEBUG',
    'display_settings': {
        'lines': 6,
        'separator': '|',
        'filter': 'GET'
    }
}


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


log_file_name = defaults.get('log_file_name')
logging_level_str = defaults.get('logging_level_str')
display_settings = defaults.get('display_settings')


def read_config():
    try:
        with open('lab6.config') as f:
            read_data = f.read()

            for line in read_data.split("\n"):
                global log_file_name
                global logging_level_str
                global display_settings

                if re.match("^(name=)(.*)", line):
                    log_file_name = line.split("=")[-1]
                elif re.match("^(debug=)(.*)", line):
                    logging_level_str = line.split("=")[-1]
                elif re.match("^(lines=)(.*)", line):
                    display_settings['lines'] = int(line.split("=")[-1])
                elif re.match("^(.*=)(.*)", line):
                    display_settings[line.split("=")[0]] = line.split("=")[-1]

    except FileNotFoundError:
        print('Error: Config file not found.')
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)


def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


def read_log(log_path: str):
    log_lines = list()

    try:
        file_content = read_file(log_path)
        lines = file_content.split('\n')

        for line in lines:
            # check if line not empty
            if line:
                log_lines.append(line)

        return log_lines
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


def parse_log_lines(log_lines: List):
    parsed_data = list()

    # source - https://stackoverflow.com/a/47095348
    HOST = r'^(?P<ip_address>.*?)'
    SPACE = r'\s'
    IDENTITY = r'\S+'
    USER = r'\S+'
    TIME = r'(?P<timestamp>\[.*?\])'
    REQUEST = r'\"(?P<request_method>.*?)\"'
    STATUS = r'(?P<status_code>\d{3})'
    SIZE = r'(?P<response_size>\S+)'

    REGEX = HOST + SPACE + IDENTITY + SPACE + USER + SPACE + TIME + SPACE + REQUEST + SPACE + STATUS + SPACE + SIZE + SPACE

    for line in log_lines:
        match = re.search(REGEX, line)

        ip_address = match.group('ip_address')
        timestamp = strptime(match.group('timestamp'), "[%d/%b/%Y:%H:%M:%S %z]")
        request_method = match.group('request_method')
        status_code = int(match.group('status_code'))

        response_size_str = match.group('response_size')
        response_size = int(match.group('response_size')) if response_size_str != "-" else None

        parsed_data.append((ip_address, timestamp, request_method, status_code, response_size))

    return parsed_data


def ip_int_to_binary_string(ip_address: str):
    result = ''

    for octet in ip_address.split("."):
        result += '{:08b}'.format(int(octet))

    return result


def is_host_in_network(host_ip: str, network_ip: str, mask_size: int):
    host = ip_int_to_binary_string(host_ip)
    network = ip_int_to_binary_string(network_ip)

    for i in range(0, mask_size):
        if host[i] is not network[i]:
            return False

    return True


def get_subnet_log_lines(parsed_log_lines: List):
    # subnet mask length:
    # 254597 % 16 + 8 = 13
    # 11111111.11111000.00000000.00000000

    # random network from the log file
    network_ip = "192.240.0.0"

    return [line for line in parsed_log_lines if is_host_in_network(line[0], network_ip, 13)]


def print_list_paginated(list_to_print: List, page_size=None):
    if page_size <= 0:
        raise ValueError(f"Page size has to be greater than 0.")

    print("[START]")
    for i, line in enumerate(list_to_print):
        if i % page_size == 0 and i != 0:
            input("Press ENTER to show more.")
            print(line)
        else:
            print(line)
    print("[END]")


def get_total_bytes_sent(parsed_log_lines: List, request_method: str):
    result = 0

    for line in parsed_log_lines:
        if re.match(rf"^({request_method})", line[2]):
            result += line[4] if line[4] else 0

    return result


def run():
    read_config()
    set_logging_level(logging_level_str)

    # print(log_file_name)
    # print(display_settings)
    #
    # print(logger.level)

    log_lines = read_log(log_file_name)
    # print(log_lines)

    parsed_log_lines = parse_log_lines(log_lines)
    # print(parsed_log_lines)

    subnet_log_lines = get_subnet_log_lines(parsed_log_lines)
    # print_list_paginated(subnet_log_lines, display_settings.get('lines'))

    total_bytes_sent = get_total_bytes_sent(parsed_log_lines, display_settings.get('filter'))
    print(f"Request method {display_settings.get('filter')} {display_settings.get('separator')} {total_bytes_sent} bytes sent in total")


if __name__ == "__main__":
    run()
