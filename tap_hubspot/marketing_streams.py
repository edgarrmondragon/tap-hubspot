"""Stream type classes for tap-hubspot."""
# from black import Report
import requests
import singer
import json

from dateutil import parser
import datetime, pytz
import time

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from memoization import cached

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_hubspot.client import HubspotStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
utc=pytz.UTC

from schemas.marketing import (
    emails
)
class MarketingStream(HubspotStream):
    records_jsonpath = "$.objects[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.offset"  # Or override `get_next_page_token`.
    replication_key = "updatedAt"
    replication_method = "INCREMENTAL"
    cached_schema = None
    properties = []
    schema_filepath = ""

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure.
        Returns row, or None if row is to be excluded"""

        if self.replication_key:
            if row[self.replication_key] <= int(time.time()):
                return None
        return row

class MarketingEmailsStream(MarketingStream):
    version = "v1"
    name = "marketing_emails"
    path = f"/marketing-emails/{version}/emails"
    primary_keys = ["id"]
    schema_filepath = ""
    replication_key = "updated"


    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['orderBy'] = "created"
        return params


    schema = emails.emails_schema
