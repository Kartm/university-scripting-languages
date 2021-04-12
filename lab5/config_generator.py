import json


def retrieve_log_file_name():
    return input("Log file name: ")


def retrieve_http_request_method():
    allowed_methods = ["GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "OPTIONS", "CONNECT", "PATCH"]

    result = input(f"HTTP request method [{', '.join(allowed_methods)}]: ")
    while result not in allowed_methods:
        print("Error: Request method not recognized. Try again. ")
        result = input(f"HTTP request method [{', '.join(allowed_methods)}]: ")

    return result


def retrieve_logging_level():
    allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    result = input(f"Logging level [{', '.join(allowed_levels)}]: ")
    while result not in allowed_levels:
        print("Error: Logging level not recognized. Try again. ")
        result = input(f"Logging level [{', '.join(allowed_levels)}]: ")

    return result


def retrieve_log_page_size():
    result = input(f"Log page size [>0]: ")
    while not result.isnumeric() or int(result) <= 0:
        print("Error: Log page size has to be a positive number. Try again. ")
        result = input(f"Log page size [>0]: ")

    return int(result)


def retrieve_resource_path():
    return input(f"Resource path: ")


def run():
    configuration = {
        "log_file_name": retrieve_log_file_name(),
        "http_request_method": retrieve_http_request_method(),
        "logging_level": retrieve_logging_level(),
        "log_page_size": retrieve_log_page_size(),
        "resource_path": retrieve_resource_path()
    }

    with open('config.json', 'w', encoding='utf-8') as f:
        json.dump(configuration, f)


if __name__ == "__main__":
    run()
