from bravado.client import SwaggerClient
from bravado.fido_client import FidoClient


class ESI:
    BASE_URL = "https://esi.evetech.net/"

    def __init__(self, sso=None, http_client=FidoClient()):
        self.client = SwaggerClient.from_url(
            "https://esi.evetech.net/_latest/swagger.json", http_client=http_client
        )
        self.sso = sso

    def get_character_standings(self) -> []:
        """
        Get the standings of the authenticated user.
        """
        return self.client.Character.get_characters_character_id_standings(
            character_id=self.sso.get_character_id()
        ).result()
