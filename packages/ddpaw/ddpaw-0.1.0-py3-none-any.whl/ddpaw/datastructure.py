# pypi/conda library
from datadog_api_client import ApiClient, AsyncApiClient
from datadog_api_client.configuration import Configuration as DataDogConfiguration
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    app_key: str = Field(serialization_alias="app_key", validation_alias=AliasChoices("DATADOG_APP_KEY", "DD_APP_KEY"))
    api_key: str = Field(
        serialization_alias="api_key",
        validation_alias=AliasChoices("DATADOG_API_KEY", "DD_API_KEY"),
    )
    api_host: str = Field(
        default="datadoghq.com",
        validation_alias=AliasChoices("DATADOG_API_SITE", "DD_SITE"),
    )

    def as_conf(self) -> "DataDogConfiguration":
        conf = DataDogConfiguration()
        conf.api_key["appKeyAuth"] = self.app_key
        conf.api_key["apiKeyAuth"] = self.api_key
        conf.server_variables["site"] = self.api_host
        conf.unstable_operations["query_scalar_data"] = True
        conf.unstable_operations["query_timeseries_data"] = True
        return conf

    def get_client(self) -> "ApiClient":
        return ApiClient(self.as_conf())

    def get_async_client(self) -> "AsyncApiClient":
        return AsyncApiClient(self.as_conf())
