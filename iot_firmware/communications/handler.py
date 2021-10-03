"""Module in charge of handling Messages from the external communications."""
import logging

from .schema import API_VERSION
from .schema import Version


class CommunicationsHandler:
    """Class that handles external communications.

    :param api_version: version of the api that the handler will use

    Basic usage.

    >>> api_version = Version(1, 2, 3)
    >>> communications_handler = CommunicationsHandler(api_version)
    >>> communications_handler.api_version
    1.2.3
    """

    def __init__(self, api_version: Version = API_VERSION):
        self.api_version = api_version
        logging.info(f"using api version {api_version}")
