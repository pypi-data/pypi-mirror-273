from typing import Dict, Tuple

from ..assets import TableauRevampAsset

QUERY_TEMPLATE = """
{{
  {resource}Connection(first: {page_size}, after: AFTER_TOKEN_SIGNAL) {{
    nodes {{ {fields}
    }}
    pageInfo {{
      hasNextPage
      endCursor
    }}
    totalCount
  }}
}}
"""

_COLUMNS_QUERY = """
downstreamDashboards { id }
downstreamFields { id }
downstreamWorkbooks { id }
id
name
table { id }
"""

_DASHBOARDS_QUERY = """
createdAt
id
name
path
tags { name }
updatedAt
workbook { id }
"""

_DATASOURCES_QUERY = """
__typename
createdAt
downstreamDashboards { id }
downstreamWorkbooks { id }
id
name
updatedAt
... on PublishedDatasource {
    description
    luid
    owner { luid }
    site { name }
    tags { name }
    uri
}
"""

_TABLES_QUERY = """
__typename
downstreamDashboards { id }
downstreamDatasources { id }
downstreamWorkbooks { id }
id
name
... on DatabaseTable {
    connectionType
    fullName
    schema
    tableType
}
... on CustomSQLTable {
    query
}
"""


_WORKBOOKS_QUERY = """
createdAt
description
embeddedDatasources { id }
id
luid
name
owner { luid }
projectLuid
site { name }
tags { name }
updatedAt
uri
"""

_FIELDS_QUERY = """
__typename
datasource { id }
description
downstreamDashboards { id }
downstreamWorkbooks { id }
folderName
id
name
... on DataField {
    dataType
    role
}
... on ColumnField {
    columns {
        name
        table { name }
    }
}
"""

_SHEETS_QUERY = """
containedInDashboards { id }
createdAt
id
index
name
updatedAt
upstreamFields { name }
workbook { id }
"""


GQL_QUERIES: Dict[TableauRevampAsset, Tuple[str, str]] = {
    TableauRevampAsset.COLUMN: ("columns", _COLUMNS_QUERY),
    TableauRevampAsset.DASHBOARD: ("dashboards", _DASHBOARDS_QUERY),
    TableauRevampAsset.DATASOURCE: ("datasources", _DATASOURCES_QUERY),
    TableauRevampAsset.FIELD: ("fields", _FIELDS_QUERY),
    TableauRevampAsset.SHEET: ("sheets", _SHEETS_QUERY),
    TableauRevampAsset.TABLE: ("tables", _TABLES_QUERY),
    TableauRevampAsset.WORKBOOK: ("workbooks", _WORKBOOKS_QUERY),
}
