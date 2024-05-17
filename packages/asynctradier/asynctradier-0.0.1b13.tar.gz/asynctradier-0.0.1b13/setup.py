# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asynctradier',
 'asynctradier.clients',
 'asynctradier.common',
 'asynctradier.exceptions',
 'asynctradier.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.9.1,<4.0.0', 'strenum>=0.4.15,<0.5.0', 'websockets>=12.0,<13.0']

setup_kwargs = {
    'name': 'asynctradier',
    'version': '0.0.1b13',
    'description': 'Async api wrapper for [Tradier](https://documentation.tradier.com/).',
    'long_description': '# asynctradier\n\n[![codecov](https://codecov.io/gh/jiak94/asynctradier/graph/badge.svg?token=T66WaJLNDd)](https://codecov.io/gh/jiak94/asynctradier)\n[![PyPI version](https://badge.fury.io/py/asynctradier.svg)](https://badge.fury.io/py/asynctradier)\n![Test](https://github.com/jiak94/asynctradier/actions/workflows/run_test.yaml/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/asynctradier/badge/?version=latest)](https://asynctradier.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/asynctradier)\n\nAsync api wrapper for [Tradier](https://documentation.tradier.com/).\n\nThis is _NOT_ an official package of Tradier.\n\n## Install\n\n`pip install asynctradier`\n\nif your are using poetry\n\n`poetry add asynctradier`\n\n## Documentation\n\n[Read The Doc](https://asynctradier.readthedocs.io/en/latest/)\n\n## Supported API\n\n### Account\n\n:white_check_mark: Get User Profile\n\n:white_check_mark: Get Balances\n\n:white_check_mark: Get Positions\n\n:white_check_mark: Get History\n\n:white_check_mark: Get Gain/Loss\n\n:white_check_mark: Get Orders\n\n:white_check_mark: Get an Order\n\n### Trading\n\n:white_check_mark: Modify Order\n\n:white_check_mark: Cancel Order\n\n:white_check_mark: Place Equity Order\n\n:white_check_mark: Place Option Order\n\n:white_check_mark: Place Multileg Order\n\n:white_check_mark: Place Combo Order\n\n:white_square_button: Place OTO Order\n\n:white_square_button: Place OCO Order\n\n:white_square_button: Place OTOCO Order\n\n### Market Data\n\n:white_check_mark: Get Quotes\n\n:white_check_mark: Get Option Chains\n\n:white_check_mark: Get Option Strikes\n\n:white_check_mark: Get Option Expirations\n\n:white_check_mark: Lookup Option Symbols\n\n:white_check_mark: Get Historical Quotes\n\n:white_check_mark: Get Time and Sales\n\n:white_check_mark: Get ETB Securities\n\n:white_square_button: Get Clock\n\n:white_check_mark: Get Calendar\n\n:white_check_mark: Search Companies\n\n:white_check_mark: Lookup Symbol\n\n### Streaming\n\n:white_check_mark: Market WebSocket\n\n:white_check_mark: Account WebSocket\n',
    'author': 'Jiakuan Li',
    'author_email': 'jiakuan.li.cs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
