import time
from contextlib import contextmanager

import requests
from prefect.blocks.core import Block
from pydantic import PrivateAttr
from pydantic.v1 import SecretStr
from pydantic.fields import ModelPrivateAttr


class AadClientCredentials(Block):
    """Azure Active Directory (AAD) client credentials block which allows users
    to authenticate with AAD using client credentials.
    """

    _block_type_name = "Azure AD Client Credentials"
    _logo_url = "https://stprododpcmscdnendpoint.azureedge.net/assets/icons/aad.png"  # type: ignore

    client_id: SecretStr

    client_secret: SecretStr

    token_url: str

    scope: SecretStr

    grant_type: str = "client_credentials"

    token_leeway: int = 60

    _token: str = PrivateAttr(None)
    _expiry_time: int = PrivateAttr(None)

    def block_initialization(self) -> None:
        self.get_token()

    def get_token(self) -> str:
        if (
            self._token is None
            or type(self._expiry_time) == ModelPrivateAttr
            or self._expiry_time + self.token_leeway < time.time()
        ):
            self._token = self._get_token()
        return self._token

    def _get_token(self) -> str:
        response = requests.post(
            self.token_url,
            data={
                "client_id": self.client_id.get_secret_value(),
                "client_secret": self.client_secret.get_secret_value(),
                "scope": self.scope.get_secret_value(),
                "grant_type": self.grant_type,
            },
        )
        response.raise_for_status()
        response_data = response.json()
        try:
            self._expiry_time = response_data["expires_on"]
        except KeyError:
            self._expiry_time = time.time() + response_data["expires_in"]
        return response_data["access_token"]

    def _auth_callback(self, request: requests.PreparedRequest) -> requests.PreparedRequest:
        request.headers.update({"Authorization": f"Bearer {self.get_token()}"})
        return request

    @contextmanager
    def session(self) -> requests.Session:
        session = requests.Session()
        session.auth = self._auth_callback

        yield session
        session.close()
