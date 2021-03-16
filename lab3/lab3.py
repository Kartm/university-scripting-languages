import math
import sys
import logging

logger = logging.getLogger('lab2')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def successful_reads(entries):
    result = []
    for entry in entries:
        # success codes start with 2
        if entry[1] // 100 == 2:
            result.append(entry)

    logger.debug(f'There are {len(result)} successful reads')

    return result


def failed_reads(entries):
    client_errors = []
    server_errors = []

    for entry in entries:
        # client error codes start with 2
        if entry[1] // 100 == 4:
            client_errors.append(entry)
        elif entry[1] // 100 == 5:
            server_errors.append(entry)

    logger.debug(f'There are {len(client_errors)} 4xx codes and {len(server_errors)} 5xx codes')

    return client_errors + server_errors


def html_entries(entries):
    successful_entries = successful_reads(entries)

    result = []
    for entry in successful_entries:
        path = entry[0]
        extension = path.split('.')[-1]

        if extension == 'html':
            result.append(entry)

    return result


def print_html_entries(entries):
    print(html_entries(entries))


# returns list containing entries from the log
def read_log():
    lines = sys.stdin.read().split('\n')

    entries = []
    for rawLine in lines:
        if rawLine:
            line = rawLine.split(" ")
            path = line[0]
            status_code = int(line[1])
            resource_size = int(line[2])
            resource_time = int(line[3])
            entry = (path, status_code, resource_size, resource_time)

            entries.append(entry)

    logger.debug(f'Found {len(lines)} lines in the file')
    logger.debug(f'There are {len(entries)} non-empty entries')

    return entries


def run():
    entries = read_log()
    print_html_entries(entries)


if __name__ == "__main__":
    run()
