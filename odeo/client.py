from functools import cached_property

from oauthlib.oauth2 import BackendApplicationClient
from requests.adapters import BaseAdapter
from requests_oauthlib import OAuth2Session

from odeo.services.base_service import BaseService
from odeo.services.cash_service import CashService
from odeo.services.disbursement_service import DisbursementService
from odeo.services.payment_gateway_service import PaymentGatewayService
from odeo.services.sub_user_service import SubUserService

PRODUCTION_BASE_URL = 'https://api.odeo.co.id'
DEVELOPMENT_BASE_URL = 'https://odeo-core-api.dev.odeo.co.id'


class Client(BaseService):
    client: BackendApplicationClient

    def __init__(
            self,
            client_id: str,
            client_secret: str,
            signing_key: str,
            base_url: str = DEVELOPMENT_BASE_URL
    ):
        self.client = BackendApplicationClient(client_id=client_id)

        super().__init__(
            OAuth2Session(client=self.client), base_url, client_secret, signing_key
        )

    @property
    def authentication(self):
        return self._oauth

    def set_transport_adapter(self, prefix: str, adapter: BaseAdapter):
        self._oauth.mount(prefix, adapter)

    @cached_property
    def disbursement(self) -> DisbursementService:
        return DisbursementService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def payment_gateway(self) -> PaymentGatewayService:
        return PaymentGatewayService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def sub_user(self) -> SubUserService:
        return SubUserService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )

    @cached_property
    def cash(self) -> CashService:
        return CashService(
            self._oauth, self._base_url, self._client_secret, self._signing_key
        )
