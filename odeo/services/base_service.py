import time

from requests_oauthlib import OAuth2Session


class BaseService(object):
    _oauth: OAuth2Session
    _base_url: str
    _client_secret: str
    _signing_key: str

    def __init__(
            self, oauth: OAuth2Session, base_url: str, client_secret: str, signing_key: str
    ):
        self._oauth = oauth
        self._base_url = base_url
        self._client_secret = client_secret
        self._signing_key = signing_key

    def _format_validation_headers(self, signature: str):
        return {
            'X-Odeo-Timestamp': str(int(time.time())),
            'X-Odeo-Signature': signature
        }

    def request_access_token(self) -> str:
        if not self._oauth.authorized:
            self._oauth.fetch_token(
                self._base_url + '/oauth2/token',
                client_secret=self._client_secret,
                include_client_id=True
            )

        return self._oauth.access_token
