# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alchemy']

package_data = \
{'': ['*']}

install_requires = \
['netlink-alchemy>=0.0.1', 'netlink-sharepoint-base>=0.0.6']

setup_kwargs = {
    'name': 'netlink-sharepoint-alchemy',
    'version': '0.0.6',
    'description': 'Integrate Sharepoint and SQL Alchemy',
    'long_description': '# netlink-sharepoint-alchemy\n\nIntegration of Sharepoint and SQL Alchemy\n\n\nUse the pre-configured Base for Tables that reflect a Sharepoint list, and the ready-made \nORM mapped `User` to access the users of the Sharepoint.\n\n```python\nfrom netlink.sharepoint.alchemy import Base, User\n```\n\n`id` is part of `Base`.\n\nDefine a mapped list / table like this:\n\n```python\nfrom netlink.sharepoint.alchemy import Base\nfrom sqlalchemy import Column\nfrom sqlalchemy import String\nfrom netlink.alchemy import UnsignedInteger\n\n\nclass Action(Base):\n    __tablename__ = \'action\'\n    _sharepoint_list_title = "Action"\n\n    # fmt: off\n    action           = Column(String,           nullable=False, doc=\'Title\')\n    deadline         = Column(UnsignedInteger,  nullable=True, doc=\'Deadline\')\n    comment          = Column(String,           nullable=True, doc=\'Comment\')\n    # fmt: on\n```\n\nLoad data from Sharepoint (non-working, concept only)\n\n```python\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.orm import Session\n\nfrom netlink.sharepoint.base import Site\nfrom netlink.sharepoint.alchemy import Base, User\n\n\nclass ActionControl(Base):\n    pass\n\n\nif __name__ == \'__main__\':\n    engine = create_engine(f"sqlite+pysqlite:///test.sqlite3", future=True)\n    Base.metadata.create_all(engine)\n    sharepoint = Site()\n    session = Session(engine)\n\n    User.bind_to_sharepoint(sharepoint)\n    User.load_from_sharepoint_list(session)\n\n    ActionControl.bind_to_sharepoint(sharepoint)\n    ActionControl.load_from_sharepoint_list(session)\n```\n\n',
    'author': 'Bernhard Radermacher',
    'author_email': 'bernhard.radermacher@netlink-consulting.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/netlink_python/netlink-sharepoint-alchemy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<=3.12',
}


setup(**setup_kwargs)
