# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confcls']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['smart-open>=7.0.4,<8.0.0']}

setup_kwargs = {
    'name': 'confcls',
    'version': '0.0.1',
    'description': 'Class instance configurator',
    'long_description': None,
    'author': 'Václav Krpec',
    'author_email': 'vencik@razdva.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
