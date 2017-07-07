
class GigyaClientException(Exception):
    """
    Wraps the response and the Gigya error code. More info about the errors:
    http://developers.gigya.com/display/GD/Response%20Codes%20and%20Errors%20REST
    """

    def __init__(self, response):
        """
        Given the response of Gigya all needed data can be extracted.
        """
        self.response = response

        # Error message as provided by Gigya.
        self.error_message = getattr(response, 'errorMessage')

        # Error code that is associated with the error_message.
        self.error_code = getattr(response, 'errorCode')

        # Additional error data as provided by Gigya.
        self.raw_data = getattr(response, 'rawData')

        super(GigyaClientException, self).__init__('{} {}\n\n{}'.format(self.error_code, self.error_message,
                                                                        self.raw_data))


class InvalidValueException(Exception):
    """
    Raised when an invalid value is used.
    """
    pass
