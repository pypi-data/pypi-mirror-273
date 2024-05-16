import logging
from typing import Dict, Iterator, List, Optional

import tableauserverclient as TSC  # type: ignore

from ....utils import SerializedAsset
from ..assets import TableauRevampAsset
from ..constants import (
    DEFAULT_PAGE_SIZE,
    DEFAULT_TIMEOUT_SECONDS,
    TABLEAU_SERVER_VERSION,
)
from .credentials import TableauRevampCredentials
from .errors import TableauApiError
from .gql_queries import GQL_QUERIES, QUERY_TEMPLATE
from .tsc_fields import TSC_FIELDS

logger = logging.getLogger(__name__)

# these assets must be extracted via TableauServerClient
_TSC_ASSETS = (
    # only users who published content can be extracted from MetadataAPI
    TableauRevampAsset.USER,
    # projects are not available in Metadata API
    TableauRevampAsset.PROJECT,
    # view count are not available in Metadata API
    TableauRevampAsset.USAGE,
)

_CUSTOM_PAGE_SIZE: Dict[TableauRevampAsset, int] = {
    TableauRevampAsset.FIELD: 1000,
}


def _pick_fields(
    data: SerializedAsset,
    asset: TableauRevampAsset,
) -> SerializedAsset:
    fields = TSC_FIELDS[asset]

    def _pick(row: dict):
        return {field: getattr(row, field) for field in fields}

    return [_pick(row) for row in data]


def _enrich_with_tsc(
    datasources: SerializedAsset,
    tsc_datasources: SerializedAsset,
) -> SerializedAsset:
    """
    Enrich datasources with fields coming from TableauServerClient:
    - project_luid
    - webpage_url
    """

    mapping = {row["id"]: row for row in tsc_datasources}

    for datasource in datasources:
        if datasource["__typename"] != "PublishedDatasource":
            # embedded datasources are bound to workbooks => no project
            # embedded datasources cannot be accessed via URL => no webpage_url
            continue
        luid = datasource["luid"]
        tsc_datasource = mapping[luid]
        datasource["projectLuid"] = tsc_datasource["project_id"]
        datasource["webpageUrl"] = tsc_datasource["webpage_url"]

    return datasources


def gql_query_scroll(
    server,
    query: str,
    resource: str,
) -> Iterator[SerializedAsset]:
    """Iterate over GQL query results, handling pagination and cursor"""

    def _call(cursor: Optional[str]) -> dict:
        # If cursor is defined it must be quoted else use null token
        token = "null" if cursor is None else f'"{cursor}"'
        query_ = query.replace("AFTER_TOKEN_SIGNAL", token)
        answer = server.metadata.query(query_)
        if "errors" in answer:
            raise TableauApiError(answer["errors"])
        return answer["data"][f"{resource}Connection"]

    cursor = None
    while True:
        payload = _call(cursor)
        yield payload["nodes"]

        page_info = payload["pageInfo"]
        if page_info["hasNextPage"]:
            cursor = page_info["endCursor"]
        else:
            break


class TableauRevampClient:
    """
    Connect to Tableau's API and extract assets.

    Relies on TableauServerClient overlay:
    https://tableau.github.io/server-client-python/docs/
    - for connection
    - to extract Users (Metadata

    Calls the MetadataAPI, using graphQL
    https://help.tableau.com/current/api/metadata_api/en-us/reference/index.html
    """

    def __init__(
        self,
        credentials: TableauRevampCredentials,
        timeout_sec: int = DEFAULT_TIMEOUT_SECONDS,
    ):
        self._credentials = credentials
        self._server = TSC.Server(self._credentials.server_url)
        options = {"verify": True, "timeout": timeout_sec}
        self._server.add_http_options(options)
        self._server.version = TABLEAU_SERVER_VERSION
        self.errors: List[str] = []

    @staticmethod
    def name() -> str:
        return "Tableau/API"

    def _user_password_login(self) -> None:
        """Login into Tableau using user and password"""
        self._server.auth.sign_in(
            TSC.TableauAuth(
                self._credentials.user,
                self._credentials.password,
                site_id=self._credentials.site_id,
            ),
        )

    def _pat_login(self) -> None:
        """Login into Tableau using personal authentication token"""
        self._server.auth.sign_in(
            TSC.PersonalAccessTokenAuth(
                self._credentials.token_name,
                self._credentials.token,
                site_id=self._credentials.site_id,
            ),
        )

    def login(self) -> None:
        """
        Depending on the given credentials, logs-in using either:
        - user/password
        - token_name/value (Personal Access Token)
        https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_auth.htm

        Raises an error if none can be found
        """

        if self._credentials.user and self._credentials.password:
            logger.info("Logging in using user and password authentication")
            return self._user_password_login()

        if self._credentials.token_name and self._credentials.token:
            logger.info("Logging in using token authentication")
            return self._pat_login()

        raise ValueError(
            "Invalid credentials: either user/password or PAT must be provided",
        )

    def base_url(self) -> str:
        return self._credentials.server_url

    def _fetch_from_tsc(
        self,
        asset: TableauRevampAsset,
    ) -> SerializedAsset:

        if asset == TableauRevampAsset.USER:
            data = TSC.Pager(self._server.users)

        elif asset == TableauRevampAsset.PROJECT:
            data = TSC.Pager(self._server.projects)

        elif asset == TableauRevampAsset.DATASOURCE:
            data = TSC.Pager(self._server.datasources)

        elif asset == TableauRevampAsset.USAGE:
            data = TSC.Pager(self._server.views, usage=True)

        else:
            raise AssertionError(f"Fetching from TSC not supported for {asset}")

        return _pick_fields(data, asset)

    def _fetch_from_metadata_api(
        self,
        asset: TableauRevampAsset,
    ) -> SerializedAsset:
        resource, fields = GQL_QUERIES[asset]
        page_size = _CUSTOM_PAGE_SIZE.get(asset) or DEFAULT_PAGE_SIZE
        query = QUERY_TEMPLATE.format(
            resource=resource,
            fields=fields,
            page_size=page_size,
        )
        result_pages = gql_query_scroll(self._server, query, resource)
        return [asset for page in result_pages for asset in page]

    def _fetch_datasources(self) -> SerializedAsset:
        asset = TableauRevampAsset.DATASOURCE

        datasources = self._fetch_from_metadata_api(asset)
        datasource_projects = self._fetch_from_tsc(asset)

        return _enrich_with_tsc(datasources, datasource_projects)

    def fetch(
        self,
        asset: TableauRevampAsset,
    ) -> SerializedAsset:
        """
        Extract the given Tableau Asset
        """
        if asset == TableauRevampAsset.DATASOURCE:
            # both APIs are required to extract datasources
            return self._fetch_datasources()

        if asset in _TSC_ASSETS:
            # some assets can only be extracted via TSC
            return self._fetch_from_tsc(asset)

        # extract most assets via Metadata API
        return self._fetch_from_metadata_api(asset)
