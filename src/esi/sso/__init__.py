class SSO(object):
    """
        EVE Online SSO.

        https://docs.esi.evetech.net/docs/sso/
    """
    BASE_URL = "https://login.eveonline.com"

    def __init__(self, client_id, client_secret, callback_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = callback_uri

    def login(self):
        """
            Login to EVE Online SSO.
        """
        pass

    def get_character_id(self):
        """
            Get the character ID of the authenticated user.
        """
        pass