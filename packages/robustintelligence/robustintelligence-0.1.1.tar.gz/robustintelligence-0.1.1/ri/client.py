"""Client interfaces for the Robust Intelligence API"""

from ri.apiclient.api.generative_model_testing_api import GenerativeModelTestingApi
from ri.apiclient.api.firewall_api import FirewallApi
from ri.apiclient.api.firewall_instance_manager_api import FirewallInstanceManagerApi
from ri.bases.client_base import BaseClient


class RIClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(api_key_header_name="rime-api-key", *args, **kwargs)
        self._generative_validation = GenerativeModelTestingApi(self._api_client)

    @property
    def generative_validation(self) -> GenerativeModelTestingApi:
        return self._generative_validation


class FirewallClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(api_key_header_name="X-Firewall-Api-Key", *args, **kwargs)
        self._firewall = FirewallApi(self._api_client)
        self._firewall_instance_manager = FirewallInstanceManagerApi(self._api_client)

    @property
    def firewall(self) -> FirewallApi:
        return self.firewall

    @property
    def firewall_instance_manager(self) -> FirewallInstanceManagerApi:
        return self._firewall_manager
