from dataclasses import dataclass
from typing import Any

import requests
from log import get_logger

logger = get_logger(__name__)

_BASE_URL = "https://www.poewiki.net/w/api.php"

type JsonObj = dict[str, Any]


@dataclass(frozen=True)
class ResourceQuery:
    table_name: str
    fields: list[str]
    filters: dict[str, str] | None = None
    limit: int = 50
    offset: int = 0

    def next_page(self) -> "ResourceQuery":
        return ResourceQuery(
            table_name=self.table_name,
            fields=self.fields,
            filters=self.filters,
            limit=self.limit,
            offset=self.offset + self.limit,
        )


class PoeWikiConnetor:
    def __init__(self):
        pass

    def _single_query_resource(self, query: ResourceQuery) -> list[JsonObj]:
        params = {
            "action": "cargoquery",
            "tables": query.table_name,
            "fields": query.fields,
            "limit": query.limit,
            "offset": query.offset,
            "format": "json",
        }

        if query.filters is not None:
            where_queries: list[str] = []
            for key, value in query.filters.items():
                where_queries.append(f'{key}="{value}"')
            params["where"] = " AND ".join(where_queries)

        response = requests.get(_BASE_URL, params=params)
        if not response.ok:
            msg = f"Unable to retrieve data on PoE Wiki: {response.status_code} - {response.reason}"
            logger.warning(msg)
            raise RuntimeError(msg)

        return [res.get("title") for res in response.json().get("cargoquery", [])]

    def query_resource(self, *, query: ResourceQuery) -> list[JsonObj]:
        results = []
        current_querry = query
        page_size = query.limit
        last_page_len = page_size

        while last_page_len >= page_size:
            try:
                current_results = self._single_query_resource(query=current_querry)
            except Exception as exc:  # noqa: BLE001
                logger.error(f"Error on querying: {exc}")
                current_results = []

            results += current_results
            last_page_len = len(current_results)
            current_querry = current_querry.next_page()

        return results
