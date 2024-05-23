from typing import Optional, List
from app.models.text_embedding import *
from app.models import ProviderCredentials
from app.error import raise_http_error, raise_provider_api_error, ErrorCode
from config import CONFIG
from app.utils import *
import json
import aiohttp
import logging
