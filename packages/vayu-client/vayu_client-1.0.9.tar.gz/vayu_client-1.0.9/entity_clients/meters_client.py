from typing import List

from openapi_client.api.meters_api import MetersApi
from openapi_client.api_client import ApiClient
from openapi_client.models.aggregation_method import AggregationMethod
from openapi_client.models.filter import Filter
from openapi_client.models.update_meter_request_schema import \
    UpdateMeterRequestSchema


class MetersClient:
    __meters_client: MetersApi = None

    def __init__(self, api_client: ApiClient):
        self.__meters_client = MetersApi(api_client)

    def get(self, meter_id: str):
        get_meter_response = self.__meters_client.get_meter(meter_id)

        return get_meter_response.meter
    
    def list(self, limit: int = None, cursor: int = None):
        return self.__meters_client.list_meters(limit=limit, cursor=cursor)

    def update(
        self,
        id: str,
        name: str = None,
        event_name: str = None,
        aggregation_method: AggregationMethod = None,
        filter: Filter = None,
    ):
        update_meter_request = UpdateMeterRequestSchema(
            name=name,
            eventName=event_name,
            aggregationMethod=aggregation_method,
            filter=filter
        )

        update_meter_response = self.__meters_client.update_meter(id, update_meter_request)

        return update_meter_response.meter

    def delete(self, id: str):
        delete_meter_response = self.__meters_client.delete_meter(id)

        return delete_meter_response.meter
        






    # name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="The name of the meter")
    # event_name: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="The name of the event that the meter is tracking.", alias="eventName")
    # aggregation_method: Optional[EventsDryRunResponseSchemaInnerMeterWithValuesInnerAggregationMethod] = Field(default=None, alias="aggregationMethod")
    # filter: Optional[Filter] = None