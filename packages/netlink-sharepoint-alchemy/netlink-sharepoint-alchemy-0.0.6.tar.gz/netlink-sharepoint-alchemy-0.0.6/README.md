# netlink-sharepoint-alchemy

Integration of Sharepoint and SQL Alchemy


Use the pre-configured Base for Tables that reflect a Sharepoint list, and the ready-made 
ORM mapped `User` to access the users of the Sharepoint.

```python
from netlink.sharepoint.alchemy import Base, User
```

`id` is part of `Base`.

Define a mapped list / table like this:

```python
from netlink.sharepoint.alchemy import Base
from sqlalchemy import Column
from sqlalchemy import String
from netlink.alchemy import UnsignedInteger


class Action(Base):
    __tablename__ = 'action'
    _sharepoint_list_title = "Action"

    # fmt: off
    action           = Column(String,           nullable=False, doc='Title')
    deadline         = Column(UnsignedInteger,  nullable=True, doc='Deadline')
    comment          = Column(String,           nullable=True, doc='Comment')
    # fmt: on
```

Load data from Sharepoint (non-working, concept only)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from netlink.sharepoint.base import Site
from netlink.sharepoint.alchemy import Base, User


class ActionControl(Base):
    pass


if __name__ == '__main__':
    engine = create_engine(f"sqlite+pysqlite:///test.sqlite3", future=True)
    Base.metadata.create_all(engine)
    sharepoint = Site()
    session = Session(engine)

    User.bind_to_sharepoint(sharepoint)
    User.load_from_sharepoint_list(session)

    ActionControl.bind_to_sharepoint(sharepoint)
    ActionControl.load_from_sharepoint_list(session)
```

