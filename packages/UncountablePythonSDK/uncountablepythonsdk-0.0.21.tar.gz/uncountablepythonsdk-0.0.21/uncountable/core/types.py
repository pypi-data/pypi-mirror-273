import base64
import json
import typing
from dataclasses import dataclass
from enum import StrEnum
from urllib.parse import urljoin

import aiohttp
import requests

from pkgs.argument_parser import CachedParser
from pkgs.serialization_util import serialize_for_api
from uncountable.types.client_base import APIRequest, ClientMethods


@dataclass(kw_only=True)
class AuthDetailsApiKey:
    api_id: str
    api_secret_key: str


AuthDetails = AuthDetailsApiKey
