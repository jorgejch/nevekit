import dill
import os
from bravado.client import SwaggerClient
from bravado.fido_client import FidoClient
from nevekit import get_nevekit_home, logger
from nevekit.exceptions import (
    NeveKitException,
    SwaggerClientFailedToInitializeException,
    SwaggerClientNotFoundException,
)

# Constants
SWAGGER_CLIENT_FILE_NAME = "esi_fido_swagger_client.pkl"


class __SwaggerClientCache(object):
    """
    A cache for the SwaggerClient object.
    """

    def __init__(self):
        self.swagger_client = None

    def _unpickle_swagger_client(self, swagger_client_file_name) -> SwaggerClient:
        """
        Unpickle the SwaggerClient object from the nevekit home directory.

        :param swagger_client_file_name: The name of the SwaggerClient pickle file.
        :type swagger_client_file_name: str
        :return: The SwaggerClient object.
        :rtype: SwaggerClient
        """
        try:
            with open(f"{get_nevekit_home()}/{swagger_client_file_name}", "rb") as f:
                return dill.load(f)
        except FileNotFoundError as e:
            logger.warning(
                f"SwaggerClient pickle file {swagger_client_file_name} not found in the nevekit home directory."
            )
            raise e
        except Exception as e:
            logger.error(
                f"Error unpickling SwaggerClient object {swagger_client_file_name}: {e}"
            )
            # Delete the SwaggerClient pickle file from the nevekit home directory.
            self._delete_swagger_client_pickle_file(swagger_client_file_name)
            logger.warning(
                f"SwaggerClient pickle file {swagger_client_file_name} deleted from the nevekit home directory."
            )
            raise NeveKitException() from e

    def _pickle_swagger_client(self, swagger_client, swagger_client_file_name):
        """
        Pickle the SwaggerClient object to the nevekit home directory.

        :param swagger_client: The SwaggerClient object.
        :type swagger_client: SwaggerClient
        :param swagger_client_file_name: The name of the SwaggerClient pickle file.
        :type swagger_client_file_name: str
        """
        # Create the nevekit home directory if it does not exist.
        if not os.path.exists(get_nevekit_home()):
            os.makedirs(get_nevekit_home())

        # If the SwaggerClient pickle file already exists, delete it.
        if os.path.exists(f"{get_nevekit_home()}/{swagger_client_file_name}"):
            self._delete_swagger_client_pickle_file(swagger_client_file_name)

        try:
            with open(f"{get_nevekit_home()}/{swagger_client_file_name}", "wb") as f:
                dill.dump(swagger_client, f)
        except Exception as e:
            raise NeveKitException(message="Error pickling SwaggerClient object") from e

    def _delete_swagger_client_pickle_file(self, swagger_client_file_name):
        """
        Delete the SwaggerClient pickle file from the nevekit home directory.

        :param swagger_client_file_name: The name of the SwaggerClient pickle file.
        :type swagger_client_file_name: str
        """
        try:
            os.remove(f"{get_nevekit_home()}/{swagger_client_file_name}")
        except FileNotFoundError:
            logger.warning(
                f"SwaggerClient pickle file {swagger_client_file_name} not found in the nevekit home directory."
            )
        except Exception as e:
            logger.error(
                f"Error deleting SwaggerClient pickle file {swagger_client_file_name}: {e}"
            )
            raise NeveKitException(
                message="Shit happened while deleting pickled SwaggerClient object file"
            ) from e

    def get_swagger_client(self) -> SwaggerClient:
        """
        Get the SwaggerClient object.
        It tries to unpickle from the nevekit home directory first if not set.

        :return: The SwaggerClient object.
        :rtype: SwaggerClient
        """
        if self.swagger_client is None:
            try:
                self.swagger_client = self._unpickle_swagger_client(
                    SWAGGER_CLIENT_FILE_NAME
                )
                return self.swagger_client
            except FileNotFoundError as e:
                logger.warning(
                    "SwaggerClient object not found in the nevekit home directory."
                )
                raise SwaggerClientNotFoundException() from e

        return self.swagger_client

    def set_swagger_client(self, swagger_client):
        """
        Set the SwaggerClient object.

        :param swagger_client: The SwaggerClient object.
        :type swagger_client: SwaggerClient
        """
        self.swagger_client = swagger_client

        try:
            # Pickle the SwaggerClient object to the nevekit home directory.
            self._pickle_swagger_client(self.swagger_client, SWAGGER_CLIENT_FILE_NAME)
        except Exception as e:
            logger.error(f"Error pickling SwaggerClient object: {e}")
            raise NeveKitException() from e


__swagger_client_cache__ = __SwaggerClientCache()


class ESI:
    BASE_URL = "https://esi.evetech.net"
    ESI_DATASOURCE = "tranquility"

    def __init__(
        self,
        config=None,
        sso=None,
        http_client=FidoClient(),
        swagger_client_cache=__swagger_client_cache__,
    ):
        if config is None:
            config = {"ssl_verify": False}

        self.config = config
        self.sso = sso
        self.http_client = http_client
        self.swagger_client_cache = swagger_client_cache

    def init(self):
        """
        Initialize the ESI object.
        """
        try:
            self.client = SwaggerClient.from_url(
                f"{self.BASE_URL}/_latest/swagger.json?datasource={self.ESI_DATASOURCE}",
                http_client=self.http_client,
                config=self.config,
            )
        except Exception as e:
            logger.error(f"Error initializing SwaggerClient object: {e}")
            raise SwaggerClientFailedToInitializeException() from e

        try:
            self.swagger_client_cache.set_swagger_client(self.client)
        except NeveKitException as e:
            logger.warning(f"Error saving SwaggerClient object to cache: {e}")

    def get_client(self) -> SwaggerClient:
        """
        Get the SwaggerClient object.

        :return: The SwaggerClient object.
        :rtype: SwaggerClient
        """
        return self.swagger_client_cache.get_swagger_client()
