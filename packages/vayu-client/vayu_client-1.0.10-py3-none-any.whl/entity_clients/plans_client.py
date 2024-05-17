from openapi_client.api.plans_api import PlansApi
from openapi_client.api_client import ApiClient


class PlansClient:
    __plans_client: PlansApi = None

    def __init__(self, api_client: ApiClient):
        self.__plans_client = PlansApi(api_client)

    def get(self, plan_id: str):
        get_plans_response = self.__plans_client.get_plan(plan_id)

        return get_plans_response.plan
   
    def list(self, limit: int = None, cursor: int = None):
        return self.__plans_client.list_plans(limit=limit, cursor=cursor)

    def delete(self, id: str):
        delete_plan_response = self.__plans_client.delete_plan(id)

        return delete_plan_response.plan