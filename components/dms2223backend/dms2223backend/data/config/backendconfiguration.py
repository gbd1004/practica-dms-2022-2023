""" BackendConfiguration class module.
"""

from typing import Dict
from dms2223common.data.config import ServiceConfiguration


class BackendConfiguration(ServiceConfiguration):
    """ Class responsible of storing a specific backend service configuration.
    """

    def _component_name(self) -> str:
        """ The component name, to categorize the default config path.

        Returns:
            - str: A string identifying the component which will categorize the configuration.
        """

        return 'dms2223backend'

    def __init__(self):
        """ Initialization/constructor method.
        """

        ServiceConfiguration.__init__(self)

        self.set_db_connection_string('sqlite:////tmp/dms2223backend.sqlite3.db')
        self.set_service_host('127.0.0.1')
        self.set_service_port(5000)
        self.set_debug_flag(True)
        self.set_authorized_api_keys([])
        self.set_auth_service({
            'host': '127.0.0.1',
            'port': 4000,
            'apikey_secret': 'This should be the frontend API key'
        })

    def _set_values(self, values: Dict) -> None:
        """Sets/merges a collection of configuration values.

        Args:
            - values (Dict): A dictionary of configuration values.
        """
        ServiceConfiguration._set_values(self, values)

        if 'auth_service' in values:
            self.set_auth_service(values['auth_service'])
        

    def set_auth_service(self, auth_service: Dict) -> None:
        """Sets the connection parameters for the authentication service.

        Args:
            auth_service (Dict): Parameters to connect to the authentication service.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['auth_service'] = auth_service

    def get_auth_service(self) -> Dict:
        """ Gets the authentication service configuration value.

        Returns:
            - Dict: A dictionary with the value of auth_service.
        """

        return self._values['auth_service']
    
    def set_db_connection_string(self, db_connection_string: str) -> None:
        """ Sets the db_connection_string configuration value.

        Args:
            - db_connection_string: A string with the configuration value.

        Raises:
            - ValueError: If validation is not passed.
        """
        self._values['db_connection_string'] = str(db_connection_string)

    def get_db_connection_string(self) -> str:
        """ Gets the db_connection_string configuration value.

        Returns:
            - str: A string with the value of db_connection_string.
        """

        return str(self._values['db_connection_string'])
