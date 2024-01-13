import pytest
import dill as pickle
from unittest.mock import patch, MagicMock, mock_open, ANY
from nevekit import get_nevekit_home
from nevekit.esi import __SwaggerClientCache
from nevekit.exceptions import NeveKitException, SwaggerClientNotFoundException

# Constants for testing
SWAGGER_CLIENT_FILE_NAME = "esi_fido_swagger_client.pkl"
# Repetitive arguments constants
BUILTIN_OPEN = "builtins.open"
OS_REMOVE = "os.remove"
DILL_DUMP = "dill.dump"


@pytest.fixture
def swagger_client_cache():
    return __SwaggerClientCache()


def test_unpickle_swagger_client_success(swagger_client_cache):
    """
    Test that the _unpickle_swagger_client method returns the correct value.
    """

    with patch("dill.load") as mock_load:
        swagger_client = MagicMock()
        mock_load.return_value = swagger_client

        with patch(BUILTIN_OPEN, mock_open()) as mock_file:
            mock_file.return_value.__enter__.return_value = swagger_client
            result = swagger_client_cache._unpickle_swagger_client(
                SWAGGER_CLIENT_FILE_NAME
            )
            assert result == swagger_client


def test_unpickle_swagger_client_file_not_found(swagger_client_cache):
    """
    Test for handling FileNotFoundError when unpickling swagger client
    """
    with patch(BUILTIN_OPEN, mock_open()) as mock_file:
        mock_file.side_effect = FileNotFoundError()

        with pytest.raises(FileNotFoundError):
            swagger_client_cache._unpickle_swagger_client(SWAGGER_CLIENT_FILE_NAME)


def test_unpickle_swagger_client_error(swagger_client_cache):
    """
    Test for handling general exception when unpickling swagger client
    """
    with patch(BUILTIN_OPEN, mock_open()) as mock_file:
        mock_file.return_value = MagicMock()
        mock_file.return_value.__enter__.side_effect = Exception()

        with pytest.raises(NeveKitException):
            swagger_client_cache._unpickle_swagger_client(SWAGGER_CLIENT_FILE_NAME)


def test_pickle_swagger_client_success(swagger_client_cache):
    """
    Test that the _pickle_swagger_client method returns the correct value.
    """
    swagger_client = MagicMock()

    with patch("os.makedirs"):
        with patch(DILL_DUMP):
            with patch(BUILTIN_OPEN, mock_open()) as mock_file:
                swagger_client_cache._pickle_swagger_client(
                    swagger_client, SWAGGER_CLIENT_FILE_NAME
                )

                mock_file.assert_called_with(
                    f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}", "wb"
                )


def test_pickle_swagger_client_existing_file(swagger_client_cache):
    """
    Test that the _pickle_swagger_client method correctly handles an existing file.
    """
    swagger_client = MagicMock()

    with patch("os.path.exists") as mock_exists:
        with patch(OS_REMOVE) as mock_remove:
            with patch(DILL_DUMP) as mock_dump:
                with patch(BUILTIN_OPEN, mock_open()) as mock_file:
                    mock_exists.return_value = True
                    swagger_client_cache._pickle_swagger_client(
                        swagger_client, SWAGGER_CLIENT_FILE_NAME
                    )
                    mock_remove.assert_called_with(
                        f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}"
                    )
                    mock_file.assert_called_with(
                        f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}", "wb"
                    )
                    mock_dump.assert_called_with(swagger_client, ANY)


def test_delete_swagger_client_pickle_file_success(swagger_client_cache):
    """
    Verify the successful deletion of the swagger client pickle file.
    """
    with patch(OS_REMOVE) as mock_remove:
        swagger_client_cache._delete_swagger_client_pickle_file(
            SWAGGER_CLIENT_FILE_NAME
        )

        mock_remove.assert_called_with(
            f"{get_nevekit_home()}/{SWAGGER_CLIENT_FILE_NAME}"
        )


def test_delete_swagger_client_pickle_file_not_found(swagger_client_cache):
    """
    Test case to verify the behavior when the pickle file for the swagger client is not found.
    """
    with patch(OS_REMOVE) as mock_remove:
        mock_remove.side_effect = FileNotFoundError()

        swagger_client_cache._delete_swagger_client_pickle_file(
            SWAGGER_CLIENT_FILE_NAME
        )


def test_delete_swagger_client_pickle_file_error(swagger_client_cache):
    """
    Test for handling exception when deleting swagger client pickle file
    """
    with patch(OS_REMOVE) as mock_remove:
        mock_remove.side_effect = Exception()

        with pytest.raises(NeveKitException):
            swagger_client_cache._delete_swagger_client_pickle_file(
                SWAGGER_CLIENT_FILE_NAME
            )


def test_get_swagger_client_unpickled(swagger_client_cache):
    """
    Test for getting swagger client when it's already unpickled
    """
    swagger_client = MagicMock()
    swagger_client_cache.swagger_client = swagger_client

    result = swagger_client_cache.get_swagger_client()

    assert result == swagger_client


def test_get_swagger_client_not_found(swagger_client_cache):
    """
    Test for handling FileNotFoundError when getting swagger client
    """
    with patch(
        "nevekit.esi.__SwaggerClientCache._unpickle_swagger_client"
    ) as mock_unpickle:
        mock_unpickle.side_effect = FileNotFoundError()

        with pytest.raises(SwaggerClientNotFoundException):
            swagger_client_cache.get_swagger_client()


def test_set_swagger_client_success(swagger_client_cache):
    """
    Test that the set_swagger_client method returns the correct value.
    """
    swagger_client = MagicMock()

    with patch(
        "nevekit.esi.__SwaggerClientCache._pickle_swagger_client"
    ) as mock_pickle:
        swagger_client_cache.set_swagger_client(swagger_client)

        assert swagger_client_cache.swagger_client == swagger_client
        mock_pickle.assert_called_with(swagger_client, ANY)


def test_set_swagger_client_error(swagger_client_cache):
    """
    Test that the set_swagger_client method responds correctly to an error.
    """
    swagger_client = MagicMock()

    with patch(
        "nevekit.esi.__SwaggerClientCache._pickle_swagger_client"
    ) as mock_pickle:
        mock_pickle.side_effect = Exception()

        with pytest.raises(NeveKitException):
            swagger_client_cache.set_swagger_client(swagger_client)
