import re
import sys
from datetime import datetime


# source - https://stackoverflow.com/a/47095348
import pytz

HOST = r'^(?P<ip_address>.*?)'
SPACE = r'\s'
IDENTITY = r'\S+'
USER = r'\S+'
TIME = r'(?P<timestamp>\[.*?\])'
REQUEST = r'\"(?P<request>.*?)\"'
STATUS = r'(?P<status_code>\d{3})'
SIZE = r'(?P<response_size>\S+)'

LOG_REGEX = HOST + SPACE + IDENTITY + SPACE + USER + SPACE + TIME + \
        SPACE + REQUEST + SPACE + STATUS + SPACE + SIZE + SPACE


class MalformedRequestError(ValueError):
    pass


def get_datetime(raw_timestamp: str):
    return datetime.strptime(raw_timestamp, "[%d/%b/%Y:%H:%M:%S %z]")


def log_object_from_line(raw_line: str):
    match = re.search(LOG_REGEX, raw_line)

    ip_address = match.group('ip_address')
    timestamp = get_datetime(match.group('timestamp'))
    request = match.group('request')
    status_code = int(match.group('status_code'))

    response_size_str = match.group('response_size')
    response_size = int(match.group('response_size')) \
        if response_size_str != "-" else None

    return MyLogEntry(ip_address, timestamp, request, status_code, response_size)


def read_file(path: str):
    with open(path) as f:
        content = f.read()
        return content


def log_entries_from_file(log_path: str):
    malformed_requests_count = 0
    log_objects = list()

    try:
        file_content = read_file(log_path)
        lines = file_content.split('\n')

        for line in lines:
            # check if line not empty
            if line:
                try:
                    log_objects.append(log_object_from_line(line))
                except MalformedRequestError:
                    malformed_requests_count += 1

        print(f'{malformed_requests_count} malformed requests.')
        return log_objects
    except FileNotFoundError:
        print('Error: Log file not found.')
        sys.exit(0)


class MyHttpRequest:
    def __init__(self, request: str, response_size, status_code):
        if "HTTP" in request:
            self.method = request.split(" ")[0]
            self.resource = request.split(" ")[1]
            self.response_size = response_size
            self.status_code = status_code
        else:
            raise MalformedRequestError

    def __str__(self):
        return f"{self.method} {self.resource} {self.response_size} - {self.status_code}"


class MyLogEntry:
    def __init__(self, ip_address, timestamp, request, status_code, response_size):
        self.ip_address = ip_address
        self.timestamp = timestamp
        self.http_request = MyHttpRequest(request, response_size, status_code)

    def __str__(self):
        return f"{self.ip_address} {self.timestamp} {self.http_request}"


def get_requests_between(logs, start: datetime, end: datetime):
    if start > end:
        raise ValueError("Start time cannot be earlier than end time.")

    return list(filter(lambda log: log.timestamp >= start and log.timestamp <= end, logs))


def run():
    entries = log_entries_from_file("access_log-20201025.txt")
    # print(entries[0])

    start = datetime(2020, 10, 20, tzinfo=pytz.UTC)
    end = datetime(2020, 10, 21, tzinfo=pytz.UTC)

    # for log in get_requests_between(entries, start, end):
    #     print(log)


if __name__ == "__main__":
    run()
