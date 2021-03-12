import sys
import logging

logger = logging.getLogger('lab2')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#####################################

standard_input_data = sys.stdin.read()
lines = standard_input_data.split('\n')

largest_resource_size = -1
largest_resource_path = ''
largest_resource_processing_time = -1
failed_requests_count = 0
total_bytes_sent = 0
total_processing_time = 0

logger.info('Start')

# \r\n terminates stdin

for rawLine in lines:
    line = rawLine.split(' ')
    prefix = '!' if line[1] == '404' else ''
    path = line[0]
    print(f'{prefix}{path}')

    if int(line[2]) > largest_resource_size:
        largest_resource_size = int(line[2])
        largest_resource_path = line[0]
        largest_resource_processing_time = line[3]
        logger.debug(f'Found new largest resource at {line[0]} ({largest_resource_size}B)')

    if line[1] == '404':
        failed_requests_count += 1
        logger.debug(f'Failed request for {line[0]}')

    total_bytes_sent += int(line[2])
    total_processing_time += int(line[3])

print(f'Largest resource: {largest_resource_path} {largest_resource_size}B {largest_resource_processing_time}ms')
print(f'Failed requests: {failed_requests_count}')
print(f'Total data sent: {total_bytes_sent}B <=> {total_bytes_sent/1000}KB')
print(f'Mean processing time: {total_processing_time/len(lines)}ms')

logger.info('End')

# https://docs.python.org/3/library/logging.html
# https://docs.python.org/3/howto/logging.html
# https://docs.python.org/3/howto/logging-cookbook.html