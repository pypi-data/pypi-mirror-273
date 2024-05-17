from typing import List

from openapi_client.api.customers_api import CustomersApi
from openapi_client.api_client import ApiClient
from openapi_client.models.create_customer_request_schema import \
    CreateCustomerRequestSchema
from openapi_client.models.update_customer_request_schema import \
    UpdateCustomerRequestSchema


class CustomersClient:
    __customers_client: CustomersApi = None

    def __init__(self, api_client: ApiClient):
        self.__customers_client = CustomersApi(api_client)

    def get(self, customer_id: str):
        get_customer_response = self.__customers_client.get_customer(customer_id)

        return get_customer_response.customer
    
    def list(self, cursor: str = None, limit: int = None):
        return  self.__customers_client.list_customers(limit=limit, cursor=cursor)

    def create(self, name: str, alias: str):
        create_customer_request = CreateCustomerRequestSchema(name=name, alias=alias)
        create_customer_response =  self.__customers_client.create_customer(create_customer_request)

        return create_customer_response.customer

    def update(self, id: str, name: str = None, alias: str = None):
        update_customer_request = UpdateCustomerRequestSchema(name=name, alias=alias)
        update_customer_response = self.__customers_client.update_customer(id, update_customer_request)

        return update_customer_response.customer

    def delete(self, id: str):
        delete_customer_response = self.__customers_client.delete_customer(id)

        return delete_customer_response.customer