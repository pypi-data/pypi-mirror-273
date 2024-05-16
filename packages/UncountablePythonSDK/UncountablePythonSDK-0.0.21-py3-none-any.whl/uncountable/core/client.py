import base64
import json
import typing
from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urljoin

import requests

from pkgs.argument_parser import CachedParser
from pkgs.serialization_util import serialize_for_api
from uncountable.types.client_base import APIRequest, ClientMethods

from .file_upload import FileUpload, FileUploader, UploadedFile
from .types import AuthDetails, AuthDetailsApiKey

DT = typing.TypeVar("DT")


class EndpointMethod(StrEnum):
    POST = "POST"
    GET = "GET"


@dataclass(kw_only=True)
class HTTPRequestBase:
    method: EndpointMethod
    url: str
    headers: dict[str, str]
    body: typing.Optional[typing.Union[str, dict[str, str]]] = None
    query_params: typing.Optional[dict[str, str]] = None


@dataclass(kw_only=True)
class HTTPGetRequest(HTTPRequestBase):
    method: typing.Literal[EndpointMethod.GET]
    query_params: dict[str, str]


@dataclass(kw_only=True)
class HTTPPostRequest(HTTPRequestBase):
    method: typing.Literal[EndpointMethod.POST]
    body: typing.Union[str, dict[str, str]]


HTTPRequest = HTTPPostRequest | HTTPGetRequest


class Client(ClientMethods):
    _parser_map: dict[type, CachedParser] = {}
    _auth_details: AuthDetails
    _base_url: str
    _file_uploader: FileUploader

    def __init__(self, *, base_url: str, auth_details: AuthDetails):
        self._auth_details = auth_details
        self._base_url = base_url
        self._file_uploader = FileUploader(self._base_url, self._auth_details)

    def do_request(self, *, api_request: APIRequest, return_type: type[DT]) -> DT:
        http_request = self._build_http_request(api_request=api_request)
        match http_request:
            case HTTPGetRequest():
                response = requests.get(
                    http_request.url,
                    headers=http_request.headers,
                    params=http_request.query_params,
                )
            case HTTPPostRequest():
                response = requests.post(
                    http_request.url,
                    headers=http_request.headers,
                    data=http_request.body,
                    params=http_request.query_params,
                )
            case _:
                typing.assert_never(http_request)
        if response.status_code < 200 or response.status_code > 299:
            # TODO: handle_error
            pass
        cached_parser = self._get_cached_parser(return_type)
        try:
            data = response.json()["data"]
            return cached_parser.parse_api(data)
        except ValueError as err:
            # TODO: handle parse error
            raise err

    def _get_cached_parser(self, data_type: type[DT]) -> CachedParser[DT]:
        if data_type not in self._parser_map:
            self._parser_map[data_type] = CachedParser(data_type)
        return self._parser_map[data_type]

    def _build_auth_headers(self) -> dict[str, str]:
        match self._auth_details:
            case AuthDetailsApiKey():
                encoded = base64.standard_b64encode(
                    f"{self._auth_details.api_id}:{self._auth_details.api_secret_key}".encode()
                ).decode("utf-8")
                return {"Authorization": f"Basic {encoded}"}
        typing.assert_never(self._auth_details)

    def _build_http_request(self, *, api_request: APIRequest) -> HTTPRequest:
        headers = self._build_auth_headers()
        method = api_request.method.lower()
        data = {"data": json.dumps(serialize_for_api(api_request.args))}
        match method:
            case "get":
                return HTTPGetRequest(
                    method=EndpointMethod.GET,
                    url=urljoin(self._base_url, api_request.endpoint),
                    query_params=data,
                    headers=headers,
                )
            case "post":
                return HTTPPostRequest(
                    method=EndpointMethod.POST,
                    url=urljoin(self._base_url, api_request.endpoint),
                    body=data,
                    headers=headers,
                )
            case _:
                raise ValueError(f"unsupported request method: {method}")

    def upload_files(
        self: typing.Self, *, file_uploads: list[FileUpload]
    ) -> list[UploadedFile]:
        """Upload files to uncountable, returning file ids that are usable with other SDK operations."""
        return self._file_uploader.upload_files(file_uploads=file_uploads)
