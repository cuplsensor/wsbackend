from .. import ApiWrapper


class ConsumerApiWrapper(ApiWrapper):
    def __init__(self, baseurl: str, tokenstr: str = None):
        """Constructor for ConsumerApiWrapper

        Args:
            baseurl (str): Websensor backend base URL.
            tokenstr (str): OAuth access token.
        """
        super().__init__(baseurl)
        self.apiurl = "{baseurl}/api/consumer".format(baseurl=self.baseurl)


    @staticmethod
    def process_status(status_code: int, desc: str = None):
        """Raise exception if an HTTP error occurs.

        Args:
            status_code (int): `HTTP status code <https://en.wikipedia.org/wiki/List_of_HTTP_status_codes>`_.
            desc (str): Description of error.

        Returns:
            None

        """
        if status_code == 400:
            raise Exception400
        elif status_code == 401:
            raise Exception401(message=desc)
        elif status_code == 403:
            raise Exception403
        elif status_code == 404:
            raise Exception404
        elif status_code == 409:
            raise Exception409
        elif status_code > 400:
            print(status_code)
            raise ConsumerAPIException(message=desc)


class ConsumerAPIException(Exception):
    def __init__(self, message):
        super().__init__("Consumer API Error: {}".format(message))


class Exception404(Exception):
    def __init__(self, message="404 Resource not found"):
        super().__init__(message)


class Exception409(Exception):
    def __init__(self, message="409 Resource already exists"):
        super().__init__(message)


class Exception400(Exception):
    def __init__(self, message="400 Bad input"):
        super().__init__(message)


class Exception403(Exception):
    def __init__(self, message="Forbidden."):
        super().__init__(message)


class Exception401(Exception):
    def __init__(self, message="Not authorised to access this resource. "
                               "Invalid JWT or bad HMAC."):
        super().__init__("Exception 401 " + str(message))
