import json
import re
from typing import Any, Callable
from typing import Union

import httpx
import pytest_httpx

from pytest_aws_apigateway.context import LambdaContext, create_context
from pytest_aws_apigateway.integration import ResponseFormatError
from pytest_aws_apigateway.integration import IntegrationResponse
from pytest_aws_apigateway.integration import build_integration_request
from pytest_aws_apigateway.integration import transform_integration_response

__all__ = ["ApiGatewayMock"]


class ApiGatewayMock:
    def __init__(self, httpx_mock: pytest_httpx.HTTPXMock):
        self.httpx_mock = httpx_mock
        ...

    def add_integration(
        self,
        resource: str,
        method: str,
        endpoint: str,
        handler: Callable[[dict[str, Any], LambdaContext], IntegrationResponse],
    ):
        resource = self._normalize_resource(resource)
        endpoint = self._normalize_endpoint(endpoint)

        url = self._url_expression(endpoint, resource)

        def integration(request: httpx.Request) -> httpx.Response:
            event = build_integration_request(request, resource)
            context = create_context(handler)
            resp = handler(event, context)
            try:
                return transform_integration_response(resp)
            except ResponseFormatError:
                return httpx.Response(
                    status_code=500,
                    json=json.dumps({"message": "Internal server error"}),
                )

        self.httpx_mock.add_callback(callback=integration, url=url, method=method)

    def _normalize_resource(self, resource: str) -> str:
        resource = resource.lstrip("/")
        resource = f"/{resource}"
        return resource

    def _url_expression(self, endpoint: str, resource: str) -> Union[re.Pattern, str]:
        p = re.compile(r"\{([^\/]+)\}")
        res = re.subn(p, r"([^\/]+)", resource)
        return re.compile(f"{endpoint}{res[0]}")

    def _normalize_endpoint(self, endpoint: str) -> str:
        return endpoint.rstrip("/")
