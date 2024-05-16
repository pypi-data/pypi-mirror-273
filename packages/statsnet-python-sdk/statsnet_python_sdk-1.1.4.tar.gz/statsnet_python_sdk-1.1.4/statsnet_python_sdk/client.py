import json
import os
from typing import Any, Optional

import httpx

from .exceptions import ClientException, InvalidParamsException
from .validations import validate_id, validate_limit, validate_jurisdiction
from .models import (
    UserResponse,
    Search,
    CompanyResult,
    DataViewResult,
    CourtCaseResult,
    GovContractsWithMeta,
    EventsWithMeta,
    RelationResult,
)


class Client:
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("STATSNET_API_KEY")
        if not api_key:
            raise ValueError("No api key provided. Set via argument or environment variable STATSNET_API_KEY.")

        self.__client: httpx.Client = httpx.Client(
            headers={"X-API-KEY": api_key}, base_url="https://dev.statsnet.co/api/v2"
        )

    def __close(self):
        self.__client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    def __request(self, method: str, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        r = self.__client.request(method, endpoint, params=params, json=json)
        if not r.is_success:
            raise ClientException(endpoint, r.status_code, r.content)
        return r.content

    def __get(self, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        return self.__request("GET", endpoint, params, json)

    def __post(self, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        return self.__request("POST", endpoint, params, json)

    def me(self) -> UserResponse:
        r = self.__get("/user/me")
        return json.loads(r)

    def search(self, query: str, jurisdiction: Optional[str] = None, limit: int = 5) -> Search:
        if not query:
            raise InvalidParamsException("query must be of type str and not empty", "query", query)
        validate_limit(limit)
        validate_jurisdiction(True, jurisdiction)

        filters = {"jurisdiction": [jurisdiction]} if jurisdiction else {}
        r = self.__post(
            "/business/search",
            params={"limit": limit},
            json={"filters": filters, "query": query},
        )
        return json.loads(r)

    def get_company(self, jurisdiction: str, id: int) -> CompanyResult:
        validate_jurisdiction(False, jurisdiction)
        validate_id(id)
        r = self.__get(f"/business/{jurisdiction}/{id}/paid")
        return json.loads(r)

    def get_company_meta(self, id: int) -> DataViewResult:
        validate_id(id)
        r = self.__get(f"/business/{id}/data/view/meta")
        return json.loads(r)

    def get_company_court_cases(self, id: int, limit: int = 5) -> CourtCaseResult:
        validate_id(id)
        validate_limit(limit)
        r = self.__get(f"/business/{id}/court_cases", {"limit": limit})
        return json.loads(r)

    def get_company_departments(self, id: int, limit: int = 5) -> dict:
        validate_id(id)
        validate_limit(limit)
        r = self.__get(f"/business/{id}/department", {"limit": limit})
        return json.loads(r)

    def get_company_gov_contracts(self, id: int, limit: int = 5) -> GovContractsWithMeta:
        validate_id(id)
        validate_limit(limit)
        r = self.__get(f"/business/{id}/gov_contracts", {"limit": limit})
        return json.loads(r)

    def get_company_events(self, id: int, limit: int = 5) -> EventsWithMeta:
        validate_id(id)
        validate_limit(limit)
        r = self.__get(f"/business/{id}/events", {"limit": limit})
        return json.loads(r)

    def get_company_relations(self, id: int, limit: int = 5) -> RelationResult:
        validate_id(id)
        validate_limit(limit)
        r = self.__get(f"/business/{id}/relations/table", {"limit": limit})
        return json.loads(r)

    def get_company_by_identifier(self, identifier: str) -> CompanyResult:
        if not type(identifier) is str:
            raise InvalidParamsException("identifier must be of type str and not empty", "identifier", identifier)
        r = self.__get(f"/business/{identifier}/bin")
        return json.loads(r)


class AsyncClient:
    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = os.getenv("STATSNET_API_KEY")
        if not api_key:
            raise ValueError("No api key provided. Set via argument or environment variable STATSNET_API_KEY.")

        self.__client: httpx.AsyncClient = httpx.AsyncClient(
            headers={"X-API-KEY": api_key}, base_url="https://dev.statsnet.co/api/v2"
        )

    async def __close(self):
        await self.__client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__close()

    async def __request(self, method: str, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        r = await self.__client.request(method, endpoint, params=params, json=json)
        if not r.is_success:
            raise ClientException(endpoint, r.status_code, r.content)
        return r.content

    async def __get(self, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        return await self.__request("GET", endpoint, params, json)

    async def __post(self, endpoint: str, params: dict = None, json: Any = None) -> bytes:
        return await self.__request("POST", endpoint, params, json)

    async def me(self) -> UserResponse:
        r = await self.__get("/user/me")
        return json.loads(r)

    async def search(self, query: str, jurisdiction: Optional[str] = None, limit: int = 5) -> Search:
        if not query:
            raise InvalidParamsException("query must be of type str and not empty", "query", query)
        validate_limit(limit)
        validate_jurisdiction(True, jurisdiction)

        filters = {"jurisdiction": [jurisdiction]} if jurisdiction else {}
        r = await self.__post(
            "/business/search",
            params={"limit": limit},
            json={"filters": filters, "query": query},
        )
        return json.loads(r)

    async def get_company(self, jurisdiction: str, id: int) -> CompanyResult:
        validate_jurisdiction(False, jurisdiction)
        validate_id(id)
        r = await self.__get(f"/business/{jurisdiction}/{id}/paid")
        return json.loads(r)

    async def get_company_meta(self, id: int) -> DataViewResult:
        validate_id(id)
        r = await self.__get(f"/business/{id}/data/view/meta")
        return json.loads(r)

    async def get_company_court_cases(self, id: int, limit: int = 5) -> CourtCaseResult:
        validate_id(id)
        validate_limit(limit)
        r = await self.__get(f"/business/{id}/court_cases", {"limit": limit})
        return json.loads(r)

    async def get_company_departments(self, id: int, limit: int = 5) -> dict:
        validate_id(id)
        validate_limit(limit)
        r = await self.__get(f"/business/{id}/department", {"limit": limit})
        return json.loads(r)

    async def get_company_gov_contracts(self, id: int, limit: int = 5) -> GovContractsWithMeta:
        validate_id(id)
        validate_limit(limit)
        r = await self.__get(f"/business/{id}/gov_contracts", {"limit": limit})
        return json.loads(r)

    async def get_company_events(self, id: int, limit: int = 5) -> EventsWithMeta:
        validate_id(id)
        validate_limit(limit)
        r = await self.__get(f"/business/{id}/events", {"limit": limit})
        return json.loads(r)

    async def get_company_relations(self, id: int, limit: int = 5) -> RelationResult:
        validate_id(id)
        validate_limit(limit)
        r = await self.__get(f"/business/{id}/relations/table", {"limit": limit})
        return json.loads(r)

    async def get_company_by_identifier(self, identifier: str) -> CompanyResult:
        if not type(identifier) is str:
            raise InvalidParamsException("identifier must be of type str and not empty", "identifier", identifier)
        r = await self.__get(f"/business/{identifier}/bin")
        return json.loads(r)
