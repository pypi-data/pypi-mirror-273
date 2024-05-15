from ..util import is_fuzzy_key
import json

ASSET_MAP = {
    # key 都小写
    "repos": {
        "path": "repos",
        "desc": "仓库",
        "query_fields": [
            {"field": "withDocSize", "required": False, "default": True},
        ],
        "methods": {
            "list": "repos",
            "get": "repos",
            "create": {
                "path": "repos/{{ name| default(faker.word()) }}",
                "method": "post",
                "data": {
                    "name": "{{ name| default(faker.word()) }}",
                    "type": "EVENTS",
                    "groupPathNames": "数据存储/Mongodb",
                    "description": "mongodb日志存储仓库, 默认存储 15 天",
                    "retention": 1296000000,
                    "writeRefreshIntervalInSeconds": 10,
                    "shardMaxDocs": 50000000,
                    "shardMaxSizeInMB": 51200,
                    "indexMaxAgeInSecond": 86400
                }
            },
            "delete": {"path": "repos:batchDelete", "method": "post", "data": {"names": ["{{ name }}"]}}
        },
    },
    "sourcetype": {
        "path": "sourcetype",
        "desc": "来源类型",
        "methods": {
            "list": "sourcetype",
            "get": "sourcetype",
            "create": {
                "path": "sourcetype/{{ name| default(faker.word()) }}",
                "method": "post",
                "data": {
                    "name": "{{ name| default(faker.word()) }}",
                    "line": {"type": "single", "regex": ""},
                    "datetime": {
                        "type": "auto",
                        "zoneOffset": 8,
                        "dateTimeFormat": "",
                        "dateTimePrefix": "",
                        "maxDateTimeLength": 100,
                    },
                    "description": "",
                    "groupIds": [], "id": "",
                    "category": "custom",
                    "advance": {"charset": "utf-8", "fieldDiscovery": True},
                    "preset": 0,
                    "extractions": [],
                }
            },
            "delete": {
                "path": "sourcetype:batchDelete",
                "method": "post",
                "data": {
                    "names": ["{{ name }}"]
                }
            },
        }
    },
    "extractions": {
        "path": "extractions/list",
        "desc": "字段提取规则",
        "methods": {
            "list": "extractions/list",
            "get": "extractions",
            "delete": {
                "path": "extractions:batchDelete",
                "method": "post",
                "data": {
                    "ids": ["{{ id }}"]
                }
            },
            "create": {
                "path": "extractions",
                "method": "post",
                "data": {
                    "name": "{{ name }}",
                    "description": "",
                    "type": "regex",
                    "config": {
                        "pattern": "^(?<a>[\\s\\S]+)",
                        "delimiter": ",",
                        "delimiterKv": ":"
                    },
                    "sourcetype": "json",
                    "indexed": False,
                    "app": "search",
                    "schema": [
                        {
                            "field": "a"
                        }
                    ],
                    "groupIds": []
                },
            }
        },
    },
    "targets": {
        "path": "metric/targets",
        "desc": "运维资产对象",
        "methods": {
            "list": "metric/targets",
            "get": "metric/targets",
            "create": {
                "path": "metric/targets",
                "method": "post",
                "data": {
                    "targetTypeId": "_storage_switch",
                    "identities": {"name": "target_id"},
                    "names": {"name": "{{ name }}"},
                    "properties": {},
                    "customProperties": {}
                }
            },
        },
    },
    "bizsystems": {
        "path": "target/bizSystems",
        "desc": "运维资产业务系统",
        "methods": {
            "list": "target/bizSystems",
            "get": "target/bizSystems",
            "create": {"path": "metric/targets", "method": "post",
                       "data": {"targetTypeId": "_biz_system", "identities": {"biz_system": "{{ id }}"},
                                "names": {"biz_name": "{{ name }}"},
                                "properties": {
                                    "description": "{{ description| default('default descriptions') }}"},
                                "customProperties": {}}},
        }
    },
    "targettypes": {
        "path": "target/targetTypes",
        "desc": "运维资产对象类型",
        "methods": {
            "list": "target/targetTypes",
            "get": "target/targetTypes",
            "delete": {
                "path": "target/targetTypes:batchDelete",
                "method": "post",
                "data": {
                    "ids": ["{{ id }}"]
                }
            },
            "create": {
                "path": "target/targetTypes",
                "method": "post",

                "data": {
                    "name": "{{ name }}",
                    "parentId": "",
                    "displayName": "{{ name }}",
                    "identityFields": [
                        {"name": "id", "displayName": "", "type": "TEXT", "required": True}
                    ],
                    "nameFields": [
                        {"name": "name", "displayName": "",
                         "type": "TEXT", "required": True}
                    ],
                    "propertyFields": [
                        {"displayName": "", "name": "attr",
                         "required": False, "type": "TEXT"}
                    ],
                    "metricGroupIds": [],
                    "requiredMetrics": {},
                    "showMetrics": {},
                    "actions": [],
                    "logFilter": {"filter": "'id'=\"{{id}}\""},
                    "traceFilter": {"filter": "'id'=\"{{id}}\"", "repoNames": [], "associativeSwitch": False},
                    "icon": "serve_norm",
                    "app": "keta-it-asset",
                    "parentMetrics": []
                }
            },
        },
    },
    "layers": {  # 业务分层
        "path": "/apps/api/v1/keta-business-health/layers",
        "desc": "运维资产业务分层",
        "methods": {
            "list": "/apps/api/v1/keta-business-health/layers",
            "get": "/apps/api/v1/keta-business-health/layers",
            "delete": {"path": "/apps/api/v1/keta-business-health/layers:batchDelete", "method": "post",
                       "data": {"ids": ["{{ id }}"]}},
            "create": {
                "path": "/apps/api/v1/keta-business-health/layers",
                "method": "post",
                "data": {
                    "name": "{{ name }}",
                    "description": "{{ description|default('default descriptions') }}",
                    "layers": [
                        {
                            "name": "l1",
                            "icon": "layer_default",
                            "description": "层级1",
                            "targetTypes": [
                                "biz_system"
                            ]
                        },
                        {
                            "name": "l2",
                            "icon": "layer_default",
                            "description": "层级2",
                            "targetTypes": [
                                "service"
                            ]
                        }
                    ]
                }
            },
        },
    },
    "metrics": {
        "path": "metric/metrics",
        "desc": "指标",
        "methods": {
            "list": "metric/metrics",
            "get": "metric/metrics",
            "create": "metric/metrics",
        }
    },
    "users": {
        "path": "auth/users",
        "desc": "用户",
        "methods": {
            "list": "auth/users",
            "create": {"path": "auth/user", "method": "post",
                       "data": {"username": "{{ name|default(faker.name())|replace(' ', '_') }}",
                                "password": "{{ password|default('12345678') }}", "loginLimit": False,
                                "expireDays": "5",
                                "noticeTypes": [], "nickname": "",
                                "phone": "{{ phone|default(faker_zh.phone_number()) }}",
                                "roles": ["{{ role |default('general_user')}}"],
                                "mail": {"email": "{{ email |default(faker.email())}}", "smtpServer": ""},
                                "wechat": {"wechatAppId": "", "type": "member", "chatid": "", "userid": "",
                                           "partyid": "", "tagid": ""},
                                "dingDing": {"dingDingAppid": "", "type": "member", "chatid": "", "userIdList": "",
                                             "deptIdList": ""}, "groupIds": []}
                       },
            "delete": {"path": "auth/user/{{ name }}", "method": "delete"}
        }
    },
    "roles": {
        "path": "auth/roles",
        "desc": "角色",
        "methods": {
            "list": "auth/roles",
        }
    },
    "alerts": {
        "path": "alerts",
        "desc": "告警规则",
        "methods": {
            "list": "alerts",
            "get": "alerts",
        }
    },
    "nodes": {
        "path": "admin/internal/_cat/nodes",
        "desc": "节点",
        "methods": {
            "list": "admin/internal/_cat/nodes",
            "get": "admin/internal/_nodes/{{ name }}/settings",
        },
        "query_fields": [
            {"field": "h", "required": False, "default": "name"},
            {"field": "format", "required": True, "default": "json"}
        ],
        "use_default_query_params": False,
        "show_describe": False
    },
    "disk": {
        "path": "admin/disk/explain",
        "desc": "磁盘",
        "methods": {
            "list": "admin/disk/explain",
        },
        "query_fields": [
            {"field": "nodeInfo", "required": True, "default": "false"},
            {"field": "diskInfo", "required": True, "default": "true"}
        ],
        "use_default_query_params": False,
        "show_describe": False
    },
    "indices": {
        "path": "admin/internal/_cat/indices",
        "desc": "分片",
        "methods": {
            "list": {"path": "admin/internal/_cat/indices", "method": "get"},
            "get": {"path": "admin/internal/{{ name }}/_settings", "method": "get"},
            "close": {"path": "admin/internal/{{ name }}/_close", "method": "post"},
            "open": {"path": "admin/internal/{{ name }}/_open", "method": "post"},
            "delete": {"path": "admin/internal/{{ name }}", "method": "delete"}
        },
        "query_fields": [
            {"field": "h", "required": False, "default": "name"},
            {"field": "format", "required": True, "default": "json"},
            {"field": "health", "required": False, "default": "green"},
            {"field": "pri", "required": False, "default": "true"},
            {"field": "local", "required": False, "default": "false"},
            {"field": "master_timeout", "required": False, "default": "30s"},
            {"field": "ignore_unavailable", "required": False, "default": "false"},
            {"field": "allow_no_indices", "required": False, "default": "true"}
        ],
        "use_default_query_params": False,
        "show_describe": False,
    },
    "cluster": {
        "path": "admin/internal/_cat/health",
        "desc": "节点",
        "methods": {
            "list": "admin/internal/_cat/health",
        },
        "query_fields": [
            {"field": "h", "required": False, "default": "name"},
            {"field": "format", "required": True, "default": "json"},
        ],
        "use_default_query_params": False
    },
    "cluster/settings": {
        "path": "admin/internal/_cluster/settings",
        "desc": "节点",
        "methods": {
            "list": "admin/internal/_cat/health",
            "update": {
                "path": "admin/internal/_cluster/settings",
                "method": "put",
                "data": {
                    "transient": {"cluster.routing.allocation.exclude._name": "{{ name }}"}
                },
            }
        },
        "query_fields": [
            {"field": "h", "required": False, "default": "name"},
            {"field": "format", "required": True, "default": "json"},
            {"field": "include_defaults", "required": False, "default": "true"},
            {"field": "flat_settings", "required": False, "default": "true"}
        ],
        "use_default_query_params": False,  # 不使用默认查询参数，es 接口无法使用ketaops平台的默认查询参数
        "show_describe": False  # 不显示 describe 方法
    },

    # KetaAgent DC 模块
    "dc/collector/config": {
        "path": "dc/collector/config",
        "desc": "KetaAgent 采集任务配置",
        "methods": {
            "list": "dc/collector/config"
        }
    },
    "dc/collector/server/config": {
        "path": "dc/collector/server/config",
        "desc": "KetaAgent 服务端采集任务配置",
        "methods": {
            "list": "dc/collector/server/config"
        }
    },
    "dc/kubernetes/collector/rule": {
        "path": "dc/kubernetes/collector/rule",
        "desc": "KetaAgent 容器采集任务",
        "methods": {
            "list": "dc/kubernetes/collector/rule"
        }
    },
    "dc/agent": {
        "path": "dc/agent/list",
        "desc": "KetaAgent Agent实例",
        "methods": {
            "list": "dc/agent/list"
        }
    },
    "dc/tags": {
        "path": "dc/tags",
        "desc": "KetaAgent Agent标签",
        "methods": {
            "list": "dc/tags"
        }
    },
    "dc/collect/types": {
        "path": "dc/collect/types",
        "desc": "KetaAgent 采集模板",
        "methods": {
            "list": "dc/collect/types"
        }
    },
    "dc/transformer/types": {
        "path": "dc/transformer/types",
        "desc": "KetaAgent 解析模板",
        "methods": {
            "list": "dc/transformer/types"
        }
    },
    "dc/package": {
        "path": "dc/package/list",
        "desc": "KetaAgent 安装包",
        "methods": {
            "list": "dc/package/list"
        }
    },
}


def get_request_path(asset_type, method):
    path = asset_type
    data = {}
    req_method = method
    key = is_fuzzy_key(asset_type, value_map=ASSET_MAP)
    if key is None:
        return asset_type
    if "methods" in ASSET_MAP[key] and method in ASSET_MAP[key]["methods"]:
        if isinstance(ASSET_MAP[key]["methods"][method], dict):
            path = ASSET_MAP.get(key)["methods"][method]["path"]
            req_method = ASSET_MAP.get(key)["methods"][method]["method"]
            data = ASSET_MAP.get(key)["methods"][method].get("data", {})
        else:
            path = ASSET_MAP.get(key)["methods"][method]
    else:
        path = ASSET_MAP.get(key)["path"]
    return path, req_method, data


def get_resources():
    return ASSET_MAP


def get_resource(asset_type):
    return ASSET_MAP.get(asset_type)
