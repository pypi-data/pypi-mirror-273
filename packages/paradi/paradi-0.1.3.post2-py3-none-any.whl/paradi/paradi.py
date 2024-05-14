# %% imports
import requests
from .logging_config import logger
from abc import ABC, abstractmethod


# %% main class
class Paradi(ABC):
    """
    Python Abstract Restful API Dialoger Interface

    :param entry: entry point of the API (URL)
    :type entry: str
    :param login_uri: URI of the login endpoint
    :type login_uri: str
    :param logout_uri: URI of the logout endpoint
    :type logout_uri: str
    :param login_kwargs: dictionary of keyword arguments for the login endpoint
    :type login_kwargs: dict
    """

    entry: str
    loginURI: str
    logoutURI: str
    login_kwargs: dict
    session: requests.Session

    def __init__(self,
                 entry: str,
                 login_uri: str,
                 logout_uri: str,
                 login_kwargs: dict = None):

        if login_kwargs is None:
            login_kwargs = dict()
        self.entry = entry
        self.loginURI = login_uri
        self.logoutURI = logout_uri
        self.login_kwargs = login_kwargs
        self.session = requests.session()

    def __enter__(self):
        try:
            response = self.__request(verb="POST", ressource=self.loginURI, **self.login_kwargs)  # connection attempt
        except Exception as e:
            raise ConnectionAbortedError('Failed to initialise APIDialog connection') from e
        else:
            self._save_auth(response)
            logger.info("successfully connected to API using credentials")
            return self

    def __exit__(self,
                 exc_type,
                 exc_val,
                 exc_tb
                 ):
        if exc_type:  # an error occurred during the `with` statement
            raise IOError(f"The following error occurred during API dialog :\n" +
                          f"{exc_type} : {exc_val}\n" +
                          f"{exc_tb}")
        elif self.logoutURI:
            try:
                self.__request("GET", self.logoutURI)  # deconnect from the API
            except Exception as e:
                raise ConnectionError('Failed to close APIDialog connection') from e
            else:
                logger.info("successfully disconnected from API")
        else:
            logger.info("dialoger closed")

    @classmethod
    def __new__(cls, *args, **kwargs):
        if cls is Paradi:
            raise TypeError(f"Cannot create an instance of '{cls.__name__}' because it is an abstract class")
        else:
            return object.__new__(cls)

    def __request(self,
                  verb: str,
                  ressource: str,
                  **kwargs
                  ) -> requests.Response:
        """
        private method to access the API's ressources

        :param verb: http verb to use
        :type verb: str
        :param ressource: the endpoint to access
        :type ressource: str

        :return: the response from the API
        :raises: ConnectionError
        """

        if len(kwargs) > 0:
            logger.debug(f"{verb} request sent at {self.entry}/{ressource} with kwargs {tuple(kwargs)}")
        else:
            logger.debug(f"{verb} request sent at {self.entry}/{ressource}")

        response = self.session.request(verb, self.entry + "/" + ressource, **kwargs)

        match response.status_code:
            case code if 200 <= code < 300:
                return response
            case _:
                raise ConnectionError(f'{response.status_code} {response.reason}')

    def _request(self,
                 verb: str,
                 ressource: str,
                 **kwargs
                 ) -> requests.Response:
        """
        use a custom verb to interact with the API

        :param verb: the verb to use
        :type verb: str
        :param ressource: the endpoint to call
        :type ressource: str

        :return: the API's response
        """

        if verb.upper() not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
            raise ValueError(f"{verb.upper()} is not a valid HTTP method")

        if response := self.__request(verb=verb.upper(),
                                      ressource=ressource,
                                      **kwargs):
            return response

    def get(self,
            ressource: str,
            **kwargs
            ) -> requests.Response:
        """
        get a ressource from the API

        :param ressource: the endpoint to call
        :type ressource: str

        :return: the API's response
        """

        if response := self.__request(verb="GET",
                                      ressource=ressource,
                                      **kwargs):
            return response

    def post(self,
             ressource: str,
             **kwargs
             ) -> requests.Response:
        """
        post information to the API

        :param ressource: the endpoint to call
        :type ressource: str

        :return: the API's response
        """

        if response := self.__request(verb="POST",
                                      ressource=ressource,
                                      **kwargs):
            return response

    @abstractmethod
    def _save_auth(self,
                   response: requests.Response
                   ):
        """
        This method should save any information needed to make a request to the API after the first authentication

        :param response: the response object from the call of the login endpoint
        """
        ...
