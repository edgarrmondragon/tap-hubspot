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
from tap_hubspot.schemas.marketing import CampaignIds

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

LOGGER = singer.get_logger()
utc=pytz.UTC

from tap_hubspot.schemas.marketing import (
    Emails,
    CampaignIds
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

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["offset"] = next_page_token
        params['limit'] = 100
        return params

class MarketingEmailsStream(MarketingStream):
    version = "v1"
    name = "marketing_emails"
    path = f"/marketing-emails/{version}/emails/with-statistics"
    primary_keys = ["id"]
    replication_key = "updated"


    def get_url_params(self, context: Optional[dict], next_page_token: Optional[Any]) -> Dict[str, Any]:
        params = super().get_url_params(context, next_page_token)
        params['orderBy'] = "created"
        return params


    schema = Emails.schema


class MarketingCampaignIdsStream(MarketingStream):
    version = "v1"
    records_jsonpath = "$.campaigns[*]"
    name = "campaign_ids"
    path = f"/email/public/{version}/campaigns/by-id"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    replication_key = ""

    schema = CampaignIds.schema

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "campaign_id": record["id"],
        }
        """Return a context dictionary for child streams."""
        return {
            "campaign_id": record["id"],
        }

class MarketingCampaignsStream(MarketingStream):
    version = "v1"
    records_jsonpath = "$.[*]"
    name = "campaigns"
    path = "/email/public/v1/campaigns/{campaign_id}"
    primary_keys = ["id"]
    replication_method = "FULL_TABLE"
    replication_key = ""
    parent_stream_type = MarketingCampaignIdsStream

    schema = CampaignIds.schema
