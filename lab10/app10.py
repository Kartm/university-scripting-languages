class MyHttpRequest:
    def __init__(self, request_type, resource_path, protocol_type):
        self.request_type = request_type
        self.resource_path = resource_path
        self.protocol_type = protocol_type


def reqstr2obj(request_string):
    if type(request_string) == str:
        pass
    else:
        raise TypeError("Request string has to be of type string.")
