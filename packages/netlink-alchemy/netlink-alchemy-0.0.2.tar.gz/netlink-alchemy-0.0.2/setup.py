# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alchemy']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=2.0.30']

setup_kwargs = {
    'name': 'netlink-alchemy',
    'version': '0.0.2',
    'description': 'Extensions for SQL Alchemy',
    'long_description': '# netlink-alchemy\n\nExtensions for SQL Alchemy\n\nAdditional Types (implemented for MySQL and MariaDB):\n\n- `TinyInteger`\n- `UnsignedTinyInteger`\n\n- `UnsignedSmallInteger`\n\n- `MediumInteger`\n- `UnsignedMediumInteger`\n\n- `UnsignedInteger`\n\n- `UnsignedBigInteger`\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-sharepoint',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.12',
}


setup(**setup_kwargs)
