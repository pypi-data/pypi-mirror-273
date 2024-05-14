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

entry_points = \
{'console_scripts': ['documentation = '
                     'https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/blob/main/README.md',
                     'issues = '
                     'https://github.com/LiLuo-B/nonebot-plugin-valve-server-query/issues',
                     'source = '
                     'https://github.com/LiLuo-B/nonebot-plugin-valve-server-query']}

setup_kwargs = {
    'name': 'nonebot-plugin-valve-server-query',
    'version': '0.5.0',
    'description': 'Valve server query plugin for NoneBot2',
    'long_description': None,
    'author': 'LiLuo-B',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
