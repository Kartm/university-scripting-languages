import re
import sys
import logging

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


def run():
    read_config()
    set_logging_level(logging_level_str)

    # print(log_file_name)
    # print(display_settings)
    #
    # print(logger.level)

    log_lines = read_log(log_file_name)
    print(log_lines)


if __name__ == "__main__":
    run()
