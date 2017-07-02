class FormatException(Exception):
    def __init__(self, message, string):
        super(FormatException, self).__init__('{} - string:\'{}\''.format(message, string))
        self.string = string


def assert_format(condition, message, string):
    if not condition:
        raise FormatException(message, string)
