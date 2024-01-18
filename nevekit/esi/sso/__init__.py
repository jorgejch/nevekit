import secrets
import threading
import webbrowser

from datetime import datetime, timedelta
from nevekit import logger
from flask import Flask, redirect, request
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7523 import ClientSecretJWT

BASE_URL = "https://login.eveonline.com"
API_VERSION = "v2"
TOKEN_ENDPOINT = f"{BASE_URL}/{API_VERSION}/oauth/token"
AUTHORIZATION_ENDPOINT = f"{BASE_URL}/{API_VERSION}/oauth/authorize"
CALLBACK_URI = "http://localhost:5000/oauth-callback"

# Create the Flask app.
app = Flask(__name__)
csrf = CSRFProtect()
csrf.init_app(app)

app.secret_key = secrets.token_urlsafe(32)
logger.info("Created Flask app.")


class SSO(object):
    """
    EVE Online SSO.

    https://docs.esi.evetech.net/docs/sso/
    """

    def __init__(self, client_id, client_secret, callback_uri, scopes=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = callback_uri
        self.scopes = scopes if scopes else ["publicData"]

        self.oauth = None
        self.state = None
        self.code_verifier: str | None = None
        self.character_id: int | None = None
        self.access_token: str | None = None
        self.access_token_expires_at: datetime | None = None

    def _init(self):
        """
        Initialize the SSO object.
        """

        # Create the OAuth2Session object.
        self.oauth = OAuth2Session(
            self.client_id,
            self.client_secret,
            scope=self.scopes,
            redirect_uri=self.callback_uri,
            token_endpoint_auth_method=ClientSecretJWT(TOKEN_ENDPOINT),
            code_challenge_method="S256",
        )

        # Generate the code verifier.
        self.code_verifier = secrets.token_urlsafe(48)

    def _get_auth_url(self) -> str:
        """
        Get the authorization URL.
        """
        uri, self.state = self.oauth.create_authorization_url(
            AUTHORIZATION_ENDPOINT,
            respose_type="code",
            code_verifier=self.code_verifier,
        )

        return uri

    def _is_token_expired(self) -> bool:
        """
        Check if the access token is expired.
        """
        return self.access_token_expires_at <= datetime.utcnow()

    def _update_token_expires_at(self, expires_at: float):
        # Set the access token expiration time.
        self.access_token_expires_at = datetime.utcnow() + timedelta(seconds=expires_at)

    def _refresh_token(self):
        """
        Refresh the access token.
        """
        self.access_token = self.oauth.refresh_token(
            TOKEN_ENDPOINT,
            refresh_token=self.access_token["refresh_token"],
            code_verifier=self.code_verifier,
        )
        self._update_token_expires_at(float(self.access_token["expires_at"]))

    def start_auth_process(self):
        """
        Start the authentication process.
        """
        # Initialize the SSO object.
        if not self.oauth:
            self._init()

        # Start the Flask app.
        threading.Thread(target=lambda: app.run(port=5000)).start()

        # Open the EVE Online SSO login page in the default browser.
        webbrowser.open("http://localhost:5000/login")

    def get_access_token(self):
        """
        Get the access token.
        """
        # Check if the access token is expired and refresh it if necessary.
        if self._is_token_expired():
            self._refresh_token()

        return self.access_token

    def get_character_id(self) -> int:
        """
        Get the character ID of the authenticated user.

        :return: The character ID of the authenticated user.
        :rtype: int
        """
        return self.character_id

    @app.route("/login")
    def login(self):
        """
        Login to EVE Online SSO.
        """
        # Redirect the user to the EVE Online SSO login page.
        return redirect(self._get_auth_url())

    @app.route("/oauth-callback")
    def oauth_callback(self):
        """
        The OAuth2 callback URL.
        """
        # Get the authorization response.
        authorization_response = request.url

        # Get the access token.
        self.access_token = self.oauth.fetch_token(
            TOKEN_ENDPOINT,
            authoritarion_response=authorization_response,
            code_verifier=self.code_verifier,
            grant_type="authorization_code",
        )

        # Set the access token expiration time.
        self._update_token_expires_at(float(self.access_token["expires_at"]))

        # Get the character ID.
        self.character_id = self.oauth.get(
            "https://login.eveonline.com/oauth/verify"
        ).json()["CharacterID"]

        # Shutdown the Flask app.
        func = request.environ.get("werkzeug.server.shutdown")
        if func is None:
            raise RuntimeError("Not running with Werkzeug Server")
        func()
