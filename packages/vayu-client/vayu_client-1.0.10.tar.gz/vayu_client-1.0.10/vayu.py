from entity_clients.contracts_client import ContractsClient
from entity_clients.customers_client import CustomersClient
from entity_clients.events_client import EventsClient
from entity_clients.invoices_client import InvoicesClient
from entity_clients.meters_client import MetersClient
from entity_clients.plans_client import PlansClient
from openapi_client.api.auth_api import AuthApi
from openapi_client.api_client import ApiClient
from openapi_client.configuration import Configuration
from openapi_client.models.aggregation_method import AggregationMethod
from openapi_client.models.login_request_schema import LoginRequestSchema
from vayu_consts import VAYU_URL


class Vayu:
    __access_token: str = None
    __host: str

    def __init__(self, api_key: str, host: str = VAYU_URL):
        self.__host = host
        self.__login(api_key)
    

    @property
    def __private_api_client(self):
        configuration = Configuration(host=self.__host, api_key=self.__access_token)
        return ApiClient(configuration, header_name='Authorization', header_value=f'Bearer {self.__access_token}')

    @property
    def __public_api_client(self):
        configuration = Configuration(host=self.__host)
        
        return ApiClient(configuration)
    

    @property
    def customers(self)->CustomersClient:
        return CustomersClient(self.__private_api_client)

    @property
    def plans(self)->PlansClient:
        return PlansClient(self.__private_api_client)


    @property
    def contracts(self)->ContractsClient:
        return ContractsClient(self.__private_api_client)


    @property
    def meters(self)->MetersClient:
        return MetersClient(self.__private_api_client)


    @property
    def invoices(self)->InvoicesClient:
        return InvoicesClient(self.__private_api_client)

    @property
    def events(self)->EventsClient:
        return EventsClient(self.__private_api_client)

    def __login(self, refresh_token: str):
        auth_api = AuthApi(self.__public_api_client)
        login_request = LoginRequestSchema(refreshToken=refresh_token)
        refresh_response = auth_api.login(login_request)

        self.__access_token = refresh_response.access_token
