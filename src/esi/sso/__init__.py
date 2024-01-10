class SSO(object):
    BASE_URL = 'https://login.eveonline.com'

    def __init__(self, client_id, client_secret, callback_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = callback_uri

    def login(self):
        pass

    def get_character_id(self):
        pass