import arrow
import inflector
import itertools
import re

from abc import ABC, abstractmethod
from datetime import datetime
from tinydb import TinyDB, Query
import tinydb.operations as tyops

from app.config import Config
from utils.db_helper import DbHelper
# ------------------------------------------------------------------------------
# IMPORTANT NOTES:
# 1. `id` is not stored in the database as part of the record. It is "external"
#     metadata: db = {"1": { rec1 }, "2": { rec2 }, ...  }
# 2. Datetime fields are assumed to be Arrow instances in code and epoch timestamps when serialized.
# ------------------------------------------------------------------------------
class Base(ABC):
    # TODO: Don't hard-code TZ
    TIMEZONE = 'US/Eastern'

    DATABASE_NAME = None
    TABLE_NAME = "_default"

    __DATABASE = None

    def __init__(self, id=None, **kwargs):
        kwargs['id'] = id
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
            # TODO: env is not set anywhere yet
            env = cfg.get("session:env", "prod")
            doc_dir = cfg.get("session:docs_dir")

            db_name = cls.__db_name()
            if (env != "prod"):
                db_name += F"-{env}"

            cls.__DATABASE = TinyDB(F"{doc_dir}/{db_name}.json")

        return cls.__DATABASE.table(cls.TABLE_NAME)


    def _date_setter(self, date_value, null_ok=False):
        new_date = None

        if isinstance(date_value, arrow.Arrow):
            new_date = date_value
        elif isinstance(date_value, str):
            new_date = arrow.get(date_value)
            # new_date.replace(tzinfo=Base.TIMEZONE)
        elif isinstance(date_value, int):
            new_date = self._epoch_to_date_obj(date_value)
        elif not date_value and null_ok:
            new_date = None
        else:
            raise TypeError(F"Date must be of type INT, STR or Arrow; Got: {type(date_value)}")

        return new_date


    def _epoch_to_date_obj(self, ts):
        # Datetimes are assumed to be in `TIMEZONE` epoch format
        date_obj = arrow.get(datetime.fromtimestamp(ts), Base.TIMEZONE) if ts else None
        return date_obj


    def load(self):
        if self.id:
            data = self._database().get(doc_id=self.id)

            if data:
                data['id'] = data.doc_id
                self.__unserialize(data)
            else:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for loading: [{self.id}]")


    def _pre_save(self):
        pass


    def save(self):
        now = arrow.now(Base.TIMEZONE)

        if self.deleted_at:
            raise RuntimeError(F"Can't Save ... Object deleted [{self.deleted_at.humanize()}].")

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


    def delete(self, safe=False):
        if self.id:
            now = arrow.now(Base.TIMEZONE)
            self.__deleted_at = now

            try:
                if safe:
                    # Mark as deleted by setting the `deleted_at` date instead of
                    # actually removing the record.
                    self._database().update(tyops.set('deleted_at', self.__deleted_at.int_timestamp), doc_ids=[self.id])
                else:
                    self._database().remove(doc_ids=[self.id])
                    self.__id = None

            except KeyError as ke:
                raise ValueError(F"Record Not Found: [{self.id}]")
        else:
            raise ValueError(F"Valid Object ID required for deletion: [{self.id}]")


    @abstractmethod
    def _serialize(self):
        raise NotImplementedError("_serialize is an Abstract Method and must be overridden")


    def serialize(self, omit_id=False):
        # Shared Fields
        data = {
            "created_at": self.created_at.int_timestamp if self.created_at else None,
            "updated_at": self.updated_at.int_timestamp if self.updated_at else None,
            "deleted_at": self.deleted_at.int_timestamp if self.deleted_at else None
        }

        if not omit_id:
            data['id'] = self.id

        data.update(self._serialize())

        return data


    @abstractmethod
    def update(self, date):
        raise NotImplementedError("update is an Abstract Method and must be overridden")


    def __unserialize(self, data):
        # Shared Attributes
        ## ID
        self.__id = data.get('id', None)

        ## Timestamps
        self.__created_at = self._epoch_to_date_obj(data.get('created_at', None))
        self.__updated_at = self._epoch_to_date_obj(data.get('updated_at', None))
        self.__deleted_at = self._epoch_to_date_obj(data.get('deleted_at', None))

        # Model Specific
        self.update(data)


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
            if count is None:
                end = None
            else:
                end = offset + count

            db_iter = iter(docs)
            docs = itertools.islice(db_iter, offset, end)

        objs = []
        for doc in docs:
            objs.append(cls(id=doc.doc_id, **doc))

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

        for (field, value) in kwargs.items():
            # field=value
            # field=cmp:value
            # cmp can be eq|ne|gt|gte|lt|lte|btw
            #   - btw format: field=btw:value1:value2
            # NOTE: Currently `cmp` only valid for numeric searches
            parts = value.split(':', 1)
            if len(parts) == 1:
                test_op = 'eq'
                test_value = parts[0]
            elif len(parts) >= 2:
                test_op = parts[0]
                test_value = parts[1]

            if field == 'tags':
                # NOTE: Does not normalize tags for searching
                tags = test_value.replace(" ", "").split(',')
                query_parts.append(query_builder['tags'].any(tags))
            else:
                # Can search in boolean, int and string fields
                query_value = test_value
                if re.match("(true|false)", query_value, flags=re.IGNORECASE):
                    query_value = True if query_value.lower() == 'true' else False
                    query_parts.append(query_builder[field] == query_value)
                elif query_value.isdecimal() or re.match(r'\d+:\d+', query_value):
                    query_parts.append(query_builder[field].test(DbHelper.cmp_integer, test_op, query_value))
                elif query_value == 'null':
                    query_parts.append(query_builder[field] == None)
                else:
                    # Assume query_value is a string
                    query_parts.append(
                        query_builder[field].search(
                            query_value,
                            flags=re.IGNORECASE
                        )
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

        objs = []
        for doc in docs:
            objs.append(cls(id=doc.doc_id, **doc))

        return objs
