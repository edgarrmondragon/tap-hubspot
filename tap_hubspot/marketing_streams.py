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


    schema = th.PropertiesList(
      th.Property("ab", th.BooleanType),
      th.Property("abHoursToWait", th.NumberType),
      th.Property("abSampleSizeDefault", th.StringType),
      th.Property("abSamplingDefault", th.StringType),
      th.Property("abSuccessMetric", th.StringType),
      th.Property("abTestPercentage", th.NumberType),
      th.Property("abVariation", th.BooleanType),
      th.Property("absoluteUrl", th.StringType),
      th.Property("allEmailCampaignIds", th.ArrayType(th.NumberType)),
      th.Property("analyticsPageId", th.StringType),
      th.Property("analyticsPageType", th.StringType),
      th.Property("archived", th.BooleanType),
      th.Property("author", th.StringType),
      th.Property("authorAt", th.NumberType),
      th.Property("authorEmail", th.StringType),
      th.Property("authorName", th.StringType),
      th.Property("authorUserId", th.NumberType),
	  th.Property("campaign", th.StringType),
	  th.Property("campaignName", th.StringType),
	  th.Property("campaignUtm", th.StringType),
      th.Property("canSpamSettingsId", th.NumberType),
      th.Property("categoryId", th.NumberType),
      th.Property("contentTypeCategory", th.NumberType),
      th.Property("createPage", th.BooleanType),
      th.Property("created", th.NumberType),
      th.Property("createdById", th.NumberType),
      th.Property("currentState", th.StringType),
      th.Property("currentlyPublished", th.BooleanType),
      th.Property("domain", th.StringType),
      th.Property("emailBody", th.StringType),
      th.Property("emailNote", th.StringType),
      th.Property("emailTemplateMode", th.StringType),
      th.Property("emailType", th.StringType),
      th.Property("emailbodyPlaintext", th.StringType),
      th.Property("freezeDate", th.NumberType),
      th.Property("fromName", th.StringType),
      th.Property("htmlTitle", th.StringType),
      th.Property("id", th.NumberType),
      th.Property("isGraymailSuppressionEnabled", th.BooleanType),
      th.Property("isLocalTimezoneSend", th.BooleanType),
      th.Property("isPublished", th.BooleanType),
      th.Property("isRecipientFatigueSuppressionEnabled", th.BooleanType),
      th.Property("lastEditSessionId", th.NumberType),
      th.Property("lastEditUpdateId", th.NumberType),
      th.Property("maxRssEntries", th.NumberType),
      th.Property("metaDescription", th.StringType),
      th.Property("name", th.StringType),
      th.Property("pageExpiryEnabled", th.BooleanType),
      th.Property("pageRedirected", th.BooleanType),
      th.Property("portalId", th.NumberType),
      th.Property("previewKey", th.StringType),
      th.Property("processingStatus", th.StringType),
      th.Property("publishDate", th.NumberType),
      th.Property("publishImmediately", th.BooleanType),
      th.Property("publishedUrl", th.StringType),
      th.Property("replyTo", th.StringType),
      th.Property("resolvedDomain", th.StringType),
      th.Property("rssEmailByText", th.StringType),
      th.Property("rssEmailClickThroughText", th.StringType),
      th.Property("rssEmailCommentText", th.StringType),
      th.Property("rssEmailEntryTemplateEnabled", th.BooleanType),
      th.Property("scrubsSubscriptionLinks", th.BooleanType),
      th.Property("slug", th.StringType),
      th.Property("state", th.StringType),
      th.Property("subcategory", th.StringType),
      th.Property("subject", th.StringType),
      th.Property("subscriptionName", th.StringType),
      th.Property("transactional", th.BooleanType),
      th.Property("updated", th.NumberType),
      th.Property("url", th.StringType),
      th.Property("useRssHeadlineAsSubject", th.BooleanType),
    ).to_dict()
