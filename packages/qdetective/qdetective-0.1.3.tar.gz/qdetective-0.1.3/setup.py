# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qdetective']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'qdetective',
    'version': '0.1.3',
    'description': '量化大侦探-数据通道',
    'long_description': None,
    'author': 'suliang',
    'author_email': 'suliang_321@sina.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
