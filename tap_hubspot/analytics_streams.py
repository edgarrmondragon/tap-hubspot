"""Stream type classes for tap-hubspot."""
# from black import Report
from math import inf
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
from tap_hubspot.streams import ContactsStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
utc=pytz.UTC

from tap_hubspot.schemas.analytics import (
    AnalyticsViews,
)
class AnalyticsStream(HubspotStream):
    records_jsonpath = "$.[*]"  # Or override `parse_response`.
    schema_filepath = ""

class AnalyticsViewsStream(AnalyticsStream):
    name = "WebAnalytics_v3"
    path = "/events/v3/events/"
    primary_keys = ["id"]
    schema = WebAnalytics.schema
    parent_stream_type = ContactsStream
    ignore_parent_replication_key = False
    replication_key = "occurredAt"

    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params["objectType"] = "contact"
        params["objectId"] = context["contact_id"]
        return params

