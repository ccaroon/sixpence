import itertools
import re
from abc import ABC, abstractmethod
from datetime import datetime

import arrow
import inflector
import tinydb.operations as tyops
from tinydb import Query, TinyDB

import models
import utils.tools
from app.config import Config
from utils.db_helper import DbHelper


# ------------------------------------------------------------------------------
# IMPORTANT NOTES:
# 1. `id` is not stored in the database as part of the record. It is "external"
#     metadata: db = {"1": { rec1 }, "2": { rec2 }, ...  }
# 2. Datetime fields are assumed to be Arrow instances in code and epoch timestamps when serialized.
# ------------------------------------------------------------------------------
class Base(ABC):
    DATABASE_NAME = None
    TABLE_NAME = "_default"

    __DATABASE = None

    def __init__(self, id=None, **kwargs):
        kwargs["id"] = id
        self._cfg = Config()
        self.__unserialize(kwargs)

    @classmethod
    def __db_name(cls):
        if cls.DATABASE_NAME is None:
            inflect = inflector.Inflector()
            cls.DATABASE_NAME = inflect.pluralize(cls.__name__)

        return cls.DATABASE_NAME

    @property
    def id(self):
        is_valid = False
        if self.__id and isinstance(self.__id, int) and self.__id > 0:
            is_valid = True

        return self.__id if is_valid else None

    @property
    def created_at(self):
        return self.__created_at

    @property
    def updated_at(self):
        return self.__updated_at

    @property
    def deleted_at(self):
        return self.__deleted_at

    @classmethod
    def _database(cls):
        if not cls.__DATABASE:
            cfg = Config()
            env = cfg.get("session:env", "dev")
            doc_dir = cfg.get("session:docs_dir")

            db_name = cls.__db_name()
            if env != "prod":
                db_name += f"-{env}"

            cls.__DATABASE = TinyDB(f"{doc_dir}/{db_name}.json")

        return cls.__DATABASE.table(cls.TABLE_NAME)

    def _date_setter(self, date_value, *, null_ok=False):
        new_date = None

        if isinstance(date_value, arrow.Arrow):
            new_date = date_value
        elif isinstance(date_value, str):
            new_date = arrow.get(date_value, self._cfg.get("app:timezone"))
        elif isinstance(date_value, int):
            new_date = self._epoch_to_date_obj(date_value)
        elif not date_value and null_ok:
            new_date = None
        else:
            msg = f"Date must be of type INT, STR or Arrow; Got: {type(date_value)}"
            raise TypeError(msg)

        return new_date

    def _epoch_to_date_obj(self, ts):
        date_obj = arrow.get(datetime.fromtimestamp(ts), self._cfg.get("app:timezone")) if ts else None  # noqa: DTZ006
        return date_obj

    def load(self):
        if self.id:
            data = self._database().get(doc_id=self.id)

            if data:
                data["id"] = data.doc_id
                self.__unserialize(data)
            else:
                msg = f"Record Not Found: [{self.id}]"
                raise ValueError(msg)
        else:
            msg = f"Valid Object ID required for loading: [{self.id}]"
            raise ValueError(msg)

    def _pre_save(self):
        pass

    def save(self):
        now = arrow.now(self._cfg.get("app:timezone"))

        if self.deleted_at:
            msg = f"Can't Save ... Object deleted [{self.deleted_at.humanize()}]."
            raise RuntimeError(msg)

        # Pre Save
        self._pre_save()

        # Save
        if self.id:
            self.__updated_at = now
            self._database().update(self.serialize(omit_id=True), doc_ids=[self.id])
        else:
            self.__created_at = now
            self.__id = self._database().insert(self.serialize(omit_id=True))

        # Post Save
        self._post_save()

    def _post_save(self):
        pass

    def undelete(self):
        self.__deleted_at = None
        self.save()

    def delete(self, *, safe=False):
        if self.id:
            now = arrow.now(self._cfg.get("app:timezone"))
            self.__deleted_at = now

            try:
                if safe:
                    # Mark as deleted by setting the `deleted_at` date instead
                    # of actually removing the record.
                    self._database().update(tyops.set("deleted_at", self.__deleted_at.int_timestamp), doc_ids=[self.id])
                else:
                    self._database().remove(doc_ids=[self.id])
                    self.__id = None

            except KeyError:
                msg = f"Record Not Found: [{self.id}]"
                raise ValueError(msg) from None
        else:
            msg = f"Valid Object ID required for deletion: [{self.id}]"
            raise ValueError(msg)

    @abstractmethod
    def _serialize(self):
        msg = "_serialize is an Abstract Method and must be overridden"
        raise NotImplementedError(msg)

    def serialize(self, *, omit_id=False):
        # Shared Fields
        data = {
            "created_at": self.created_at.int_timestamp if self.created_at else None,
            "updated_at": self.updated_at.int_timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.int_timestamp if self.deleted_at else None,
        }

        if not omit_id:
            data["id"] = self.id

        data.update(self._serialize())

        return data

    @abstractmethod
    def update(self, date):
        msg = "update is an Abstract Method and must be overridden"
        raise NotImplementedError(msg)

    def __unserialize(self, data):
        # Shared Attributes
        ## ID
        self.__id = data.get("id", None)

        ## Timestamps
        self.__created_at = self._epoch_to_date_obj(data.get("created_at", None))
        self.__updated_at = self._epoch_to_date_obj(data.get("updated_at", None))
        self.__deleted_at = self._epoch_to_date_obj(data.get("deleted_at", None))

        # Model Specific
        self.update(data)

    def clone(self):
        cloned_type = type(self)
        cloned_obj = cloned_type(id=self.id)

        obj_data = self.serialize()
        cloned_obj.update(obj_data)

        return cloned_obj

    @classmethod
    def fetch(cls, offset=0, count=None, sort_by=None):
        docs = cls._database().all()
        # sort_by: attr1,attr2,attr3:asc|desc
        if sort_by:
            docs = DbHelper.sort(docs, sort_by)

        # Want ALL docs
        # TODO: Invert this condition and remove the else
        if offset == 0 and count is None:
            pass
        else:
            end = None if count is None else offset + count

            db_iter = iter(docs)
            docs = itertools.islice(db_iter, offset, end)

        objs = [cls(id=doc.doc_id, **doc) for doc in docs]

        return objs

    @classmethod
    def purge(cls):
        cls._database().truncate()

    @classmethod
    def count(cls):
        return len(cls._database())

    @classmethod
    def find(cls, op="or", sort_by=None, **kwargs):
        query_parts = []
        query_builder = Query()

        for field, query_str in kwargs.items():
            # field=<value>
            # field=<cmp>:<value>
            # <cmp> can be eq|ne|gt|gte|lt|lte|btw
            #   - btw format: field=btw:value1:value2
            # NOTE: Currently `cmp` only valid for numeric searches
            # See: DbHelper.parse_query
            (query_op, query_value) = DbHelper.parse_query(query_str)

            if field == "tags":
                tags = query_value.split(",")
                tags = [models.tag.Tag.normalize(tg) for tg in tags]
                query_parts.append(query_builder["tags"].any(tags))
            # Can search in boolean, int and string fields
            elif re.match("(true|false)", query_value, flags=re.IGNORECASE):
                query_value = query_value.lower() == "true"
                query_parts.append(query_builder[field] == query_value)
            elif query_op == "btw" or utils.tools.is_numeric(query_value):
                query_parts.append(query_builder[field].test(DbHelper.cmp_numeric, query_op, query_value))
            elif query_value == "null":
                query_parts.append(query_builder[field] == None)  # noqa: E711
            else:
                # Assume query_value is a string
                query_parts.append(
                    query_builder[field].search(
                        query_value,
                        flags=re.IGNORECASE,
                    ),
                )

        query = query_parts[0]
        if op == "or":
            for qp in query_parts:
                query |= qp
        elif op == "and":
            for qp in query_parts:
                query &= qp

        docs = cls._database().search(query)
        if sort_by:
            # sort_by: attr1,attr2,attr3:asc|desc
            docs = DbHelper.sort(docs, sort_by)

        objs = [cls(id=doc.doc_id, **doc) for doc in docs]

        return objs
