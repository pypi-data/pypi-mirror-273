from ..util import is_fuzzy_key
from .asset_map import ASSET_MAP
from ..base.client import ROOT_PATH


def list_assets_request(asset_name, groupId=-1, order="desc", pageNo=1,
                        pageSize=10, prefix="", sort="updateTime", lang=None, **kwargs):
    path = asset_name
    query_fields = []
    key = is_fuzzy_key(asset_name, value_map=ASSET_MAP)
    if key is not None:
        path = ASSET_MAP.get(key)["path"]
        if "query_fields" in ASSET_MAP.get(key):
            query_fields = ASSET_MAP.get(key)["query_fields"]
    use_default_query_params = ASSET_MAP.get(key, {}).get("use_default_query_params", True)

    if use_default_query_params:
        query_params = {
            "groupId": groupId,
            "order": order,
            "pageNo": pageNo,
            "pageSize": pageSize,
            "prefix": prefix,
            "sort": sort,
        }
    else:
        query_params = {}
    for finfo in query_fields:
        f = finfo["field"]
        dft = finfo["default"]
        required = finfo["required"]
        if f in kwargs:
            query_params[f] = kwargs[f]
        elif required:
            query_params[f] = dft

    custom_headers = {}
    if lang is not None and isinstance(lang, str):
        custom_headers["X-Pandora-Language"] = lang

    return {
        "path": path,
        "query_params": query_params,
        # list 操作用不到的内容
        "method": "get",
        "data": {},
        "custom_headers": custom_headers,
    }


def list_admin_request(asset_name, **kwargs):
    path = "/".join([ROOT_PATH, "admin/internal", asset_name])
    query_fields = []
    key = is_fuzzy_key(asset_name, value_map=ASSET_MAP)
    if key is not None:
        path = ASSET_MAP.get(key)["path"]
        if "query_fields" in ASSET_MAP.get(key):
            query_fields = ASSET_MAP.get(key)["query_fields"]

    query_params = {"format": "json"}
    for finfo in query_fields:
        f = finfo["field"]
        dft = finfo["default"]
        required = finfo["required"]
        if f in kwargs:
            query_params[f] = kwargs[f]
        elif required:
            query_params[f] = dft

    custom_headers = {}

    return {
        "path": path,
        "query_params": query_params,
        # list 操作用不到的内容
        "method": "get",
        "data": {},
        "custom_headers": custom_headers,
    }
