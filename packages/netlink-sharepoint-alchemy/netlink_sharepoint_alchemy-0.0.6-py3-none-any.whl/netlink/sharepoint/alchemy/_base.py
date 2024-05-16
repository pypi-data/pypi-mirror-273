import datetime

from sqlalchemy import Column
from sqlalchemy import String
from netlink.alchemy import UnsignedInteger
from sqlalchemy.orm import declarative_base

from netlink.sharepoint.base import List
from netlink.logging import logger


class _SharepointBase:
    __state = {}
    _sharepoint_list_title = ""
    _upper_case = None
    _required = None

    @classmethod
    def bind_to_sharepoint(cls, sharepoint_site):
        state = cls._get_state()
        if "sharepoint_site" in state:
            logger.warning(f"Already bound to Sharepoint at {state['sharepoint_site'].url}")
        else:
            state["sharepoint_site"] = sharepoint_site
            state["sharepoint_list"] = List(
                sharepoint_site,
                title=cls._sharepoint_list_title,
                map=cls._get_map(),
                upper_case=cls._upper_case,
                required=cls._required,
            )

    id = Column(UnsignedInteger, nullable=False, primary_key=True)

    @classmethod
    def _get_state(cls) -> dict:
        if cls not in cls.__state:
            cls.__state[cls] = {}
        return cls.__state[cls]

    @classmethod
    def _get_map(cls) -> dict:
        state = cls._get_state()
        if "map" not in state:
            # noinspection PyUnresolvedReferences
            state["map"] = {
                i: getattr(cls, i).__doc__ for i in cls._sa_class_manager.local_attrs if getattr(cls, i).__doc__
            }
        return state["map"]

    @property
    def _map(self) -> dict:
        return self._get_map()

    @classmethod
    def _get_sharepoint_site(cls):
        result = cls._get_state().get("sharepoint_site", None)
        if result is None:
            logger.error(f"Not bound to Sharepoint. Execute '{cls.__name__}.bind_to_sharepoint()' first.")
            raise AttributeError("sharepoint_site")
        return result

    @classmethod
    def _get_sharepoint_list(cls):
        result = cls._get_state().get("sharepoint_list", None)
        if result is None:
            logger.error(f"Not bound to Sharepoint. Execute '{cls.__name__}.bind_to_sharepoint()' first.")
            raise AttributeError("sharepoint_list")
        return result

    @classmethod
    def _init_converters(cls) -> dict:
        state = cls._get_state()
        sharepoint_site = cls._get_sharepoint_site()
        if "convert" not in state:
            state["convert"] = {}
            state["adapt"] = {}
            for column in sharepoint_site.get_list_columns(cls._sharepoint_list_title, hidden=True):
                if column.internal_name in cls._get_map().values():
                    if column.type_as_string == "DateTime":
                        state["convert"][column.internal_name] = lambda x: datetime.datetime.strptime(
                            x, "%Y-%m-%dT%H:%M:%SZ"
                        ).replace(tzinfo=datetime.timezone.utc)
                        state["adapt"][column.internal_name] = lambda x: x.strftime("%Y-%m-%dT%H:%M:%SZ")
        return state

    def _adapt(self, sql_column):
        state = self._init_converters()
        sharepoint_column = self._map[sql_column]
        if sharepoint_column in state["adapt"]:
            return state["adapt"][sharepoint_column](getattr(self, sql_column))
        return getattr(self, sql_column)

    @classmethod
    def _convert(cls, sharepoint_item, sql_column):
        state = cls._init_converters()
        sharepoint_column = cls._get_map()[sql_column]
        if sharepoint_column in state["convert"]:
            return state["convert"][sharepoint_column](sharepoint_item.get_property(sharepoint_column))
        return sharepoint_item.get_property(sharepoint_column)

    @classmethod
    def normalize_sharepoint_list(cls, *args, **kwargs):
        sharepoint_list = cls._get_sharepoint_list()
        sharepoint_list.rollback()
        sharepoint_list.normalize()
        sharepoint_list.commit()
        sharepoint_list.rollback()

    @classmethod
    def load_from_sharepoint_list(cls, session):
        state = cls._init_converters()
        sharepoint_list = cls._get_sharepoint_list()
        sharepoint_list.rollback()
        for i in sharepoint_list.values():
            content = dict(i)
            logger.trace(f"{content}")
            session.merge(cls(**content))
        session.commit()

    def __repr__(self):
        attributes = [sql_column for sql_column in self._map]
        attributes.insert(0, "id")
        for n in range(len(attributes)):
            # noinspection PyUnresolvedReferences
            if attributes[n].endswith("_id") and attributes[n][:-3] in self._sa_class_manager.local_attrs:
                attributes.append(attributes[n][:-3])
        return f"{self.__class__.__name__}({', '.join([f'{i}={getattr(self, i)!r}' for i in attributes])})"

    # def _sharepoint_insert(self, sharepoint_site, lazy: bool = False):
    #     data = {sharepoint_column: self._adapt(sql_column, sharepoint_site) for sql_column, sharepoint_column in self._map.items()}
    #     # noinspection PyTypeChecker
    #     logger.trace(data)
    #     target = sharepoint_site.get_list(self._sharepoint_list)
    #     item = sharepoint_site.get_list(self._sharepoint_list).add_item(data)
    #     if not lazy:
    #         item.execute_query()

    def commit_sharepoint(self, lazy: bool = False):
        sharepoint_list = self._get_sharepoint_list()
        if not self.id:
            raise AttributeError
        try:
            item = sharepoint_list[self.id]
        except KeyError:
            raise Exception(f"Item {self.id} not found")
        for column in self._map:
            item[column] = self._adapt(column)
        item.commit(lazy)


Base = declarative_base(cls=_SharepointBase)


class User(Base):
    __tablename__ = "user"

    # fmt: off
    name        = Column(String)
    family_name = Column(String)
    given_name  = Column(String)
    email       = Column(String)
    # fmt: on

    @classmethod
    def load_from_sharepoint_list(cls, session):
        users = cls._get_sharepoint_site().users
        for key in users:
            session.merge(
                cls(
                    id=key,
                    name=users[key]["name"],
                    family_name=users[key]["family_name"],
                    given_name=users[key]["given_name"],
                    email=users[key]["email"],
                )
            )
            session.commit()

    def __repr__(self):
        return (
            f"User(id={self.id!r}, "
            f"name={self.name!r}, "
            f"family_name={self.family_name!r}, "
            f"given_name={self.given_name!r}, "
            f"email={self.email!r})"
        )

    def commit_sharepoint(self, site, defer=False):
        raise NotImplemented
