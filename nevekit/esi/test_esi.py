import pytest
from unittest.mock import patch, MagicMock, ANY
from nevekit.esi import ESI


@pytest.fixture()
def esi():
    return ESI()


def test_init_success(esi):
    """
    Test that the ESI object is initialized correctly.
    """
    with patch("bravado.client.SwaggerClient.from_url") as mock_swagger_client:
        swagger_client = MagicMock()
        mock_swagger_client.return_value = swagger_client

        with patch(
            "nevekit.esi.__SwaggerClientCache.set_swagger_client"
        ) as mock_set_swagger_client:
            esi.init()

            mock_swagger_client.assert_called_with(
                f"{esi.BASE_URL}/_latest/swagger.json?datasource={esi.ESI_DATASOURCE}",
                http_client=ANY,
                config=ANY,
            )
            mock_set_swagger_client.assert_called_with(swagger_client)
