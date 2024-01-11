import pytest
import requests
from unittest.mock import patch, MagicMock, mock_open
from fuzzworks import Fuzzworks

# Constants for testing
TEST_ENDPOINT = "dump/lpOffers.txt"
TEST_DB_PATH = "sde.db"
TEST_DB_TYPE = "sqlite"


@pytest.fixture
def fuzzworks():
    return Fuzzworks()


def test_fetch_data_success(fuzzworks):
    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.content = b"test content"
        mock_get.return_value = mock_response

        response = fuzzworks.fetch_data(TEST_ENDPOINT, timeout=10)
        assert response.content == b"test content"
        mock_get.assert_called_with(f"{Fuzzworks.BASE_URL}/{TEST_ENDPOINT}", timeout=10)


def test_fetch_data_failure(fuzzworks):
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError("Error")

        with pytest.raises(requests.exceptions.HTTPError):
            fuzzworks.fetch_data(TEST_ENDPOINT)


def test_download_fuzzworks_sde_db_success(fuzzworks):
    with patch("fuzzworks.Fuzzworks.fetch_data") as mock_fetch_data:
        mock_response = MagicMock()
        mock_response.content = b"test db content"
        mock_fetch_data.return_value = mock_response

        with patch("builtins.open", mock_open()) as mock_file:
            fuzzworks.download_fuzzworks_sde_db(TEST_DB_PATH, TEST_DB_TYPE)
            mock_file.assert_called_with(TEST_DB_PATH, "wb")
            mock_file().write.assert_called_with(b"test db content")


def test_download_fuzzworks_sde_db_failure(fuzzworks):
    with patch("fuzzworks.Fuzzworks.fetch_data") as mock_fetch_data:
        mock_fetch_data.side_effect = requests.exceptions.HTTPError("Error")

        with pytest.raises(requests.exceptions.HTTPError):
            fuzzworks.download_fuzzworks_sde_db(TEST_DB_PATH, TEST_DB_TYPE)
