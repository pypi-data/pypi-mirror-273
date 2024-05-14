# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_valve_server_query']

package_data = \
{'': ['*'],
 'nonebot_plugin_valve_server_query': ['static/fonts/*',
                                       'static/icons/*',
                                       'static/images/*',
                                       'static/templates/*']}

install_requires = \
['dependencies',
 'dependencies',
 'dependencies',
 'dependencies',
 'dependencies',
 'dependencies']

setup_kwargs = {
    'name': 'nonebot-plugin-valve-server-query',
    'version': '0.5.3',
    'description': 'Valve server query plugin for NoneBot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>\n</p>\n\n\n<h1 align="center">nonebot-plugin-valve-server-query</h1>\n\n_✨ NoneBot查服插件，可用于查询V社的游戏服务器，支持不同服组的权限配置以及服务器信息在线更新✨_\n\n<p align="center">\n  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">\n    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">\n  </a>\n  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">\n  </a>\n  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</p>\n\n\n## 安装\n\n### nb-cli\n\n```shell\n待更新\n```\n\n### pip\n\n```shell\n待更新\n```\n\n### git\n\n```shell\n待更新\n```\n\n## 配置\n\n### 权限配置\n\n用于服务器信息更新相关命令，文件位于data/valve/authority.json，key为组名，value为拥有该组权限的QQ号列表\n\n示例\n\n```json\n{\n    "测试": [\n        "123456789",\n        "987654321"\n    ],\n    "test": [\n        "11111111"\n    ]\n}\n```\n\n### 服务器信息批量添加配置\n\n只需将json文件发送给机器人即可\n\n示例\n\n```json\n{\n    "组名": [\n        {\n            "id": 1,\n            "ip": "127.0.0.1:25535"\n        },\n        {\n            "id": 2,\n            "ip": "127.0.0.1:25536"\n        }\n    ],\n    "测试": [\n        {\n            "id": 1,\n            "ip": "127.0.0.1:25535"\n        }\n    ]\n}\n```\n\n\n\n## 使用\n\n| 指令    | 权限         | 相关参数                                                     |\n| ------- | ------------ | ------------------------------------------------------------ |\n| a2s添加 | 详见权限配置 | 若用户仅一个组有权限，需要提供：id ip port，若用户有多个组的权限需要提供：组名 id ip port |\n| a2s更新 | 详见权限配置 | 若用户仅一个组有权限，需要提供：id ip port，若用户有多个组的权限需要提供：组名 id ip port |\n| a2s删除 | 详见权限配置 | 若用户仅一个组有权限，需要提供：id ，若用户有多个组的权限需要提供：组名 id |\n| a2s列表 | 无           | 需要提供：组名，返回该组收录的所有ip:port                    |\n| connect | 无           | 需要提供：ip:port，返回服务器信息                            |\n| 组名    | 无           | 不加参数返回该组所有服务器信息，加id返回该服信息             |\n\n## 示例\n\n### 查组\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/group_queries.png" width="800"></img>\n\n### 查服\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_queries1.png" width="800"></img>\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_queries2.png" width="800"></img>\n\n### json快捷更新\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/file_receive.png" width="800"></img>\n\n### 服务器添加\n\n对多个组都有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_add1.png" width="800"></img>\n\n仅对一个组有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_add2.png" width="800"></img>\n\n### 服务器更新\n\n对多个组都有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_update1.png" width="800"></img>\n\n仅对一个组有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_update2.png" width="800"></img>\n\n### 服务器删除\n\n对多个组都有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_del1.png" width="800"></img>\n\n仅对一个组有权限时\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_del2.png" width="800"></img>\n\n### 服务器ip列表\n\n<img src="https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/resources/server_list.png" width="800"></img>',
    'author': 'LiLuo-B',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LiLuo-B/nonebot-plugin-valve-server-query',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
