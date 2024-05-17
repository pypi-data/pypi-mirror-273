from datetime import datetime

from openapi_client.api.contracts_api import ContractsApi
from openapi_client.api_client import ApiClient
from openapi_client.models.create_contract_request_schema import \
    CreateContractRequestSchema


class ContractsClient:
    __contracts_client: ContractsApi = None

    def __init__(self, api_client: ApiClient):
        self.__contracts_client = ContractsApi(api_client)

    def get(self, contract_id: str):
        get_contract_response = self.__contracts_client.get_contract(contract_id)

        return get_contract_response.contract
    
    def list(self, limit: int = None, cursor: int = None):
        return self.__contracts_client.list_contracts(limit=limit, cursor=cursor)

    def create(
        self,
        start_date: datetime,
        end_date: datetime,
        customer_id: str,
        plan_id: str
    ):
        create_contract_request = CreateContractRequestSchema(
            start_date=start_date,
            end_date=end_date,
            customer_id=customer_id,
            plan_id=plan_id
        )

        create_contract_response = self.__contracts_client.create_contract(create_contract_request)

        return create_contract_response.contract

    def delete(self, id: str):
        delete_contract_response = self.__contracts_client.delete_contract(id)

        return delete_contract_response.contract