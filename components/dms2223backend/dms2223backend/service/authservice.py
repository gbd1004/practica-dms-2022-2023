from typing import List, Optional, Union
import requests
from dms2223common.data import Role
from dms2223common.data.rest import ResponseData


class AuthService():
    """ REST client to connect to the authentication service.
    """

    def __init__(self,
                 host: str, port: int,
                 api_base_path: str = '/api/v1',
                 apikey_header: str = 'X-ApiKey-Auth',
                 apikey_secret: str = ''
                 ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The authentication service host string.
            - port (int): The authentication service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret