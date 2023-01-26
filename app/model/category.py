import datetime
from datetime import datetime, date
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import class_mapper
from collections import OrderedDict
from app.model import Base


class Category(Base):
    __tablename__ = 'category'

    # Columns
    _id = Column("id", Integer, primary_key=True)
    _cnt = Column('cnt', Integer)
    _title = Column('title', String)

    @property
    def id(self) -> int:
        return self._id

    @property
    def cnt(self) -> int:
        return self._cnt

    @property
    def title(self) -> str:
        return self._title

    def __init__(self, title: str, cnt: int = 1):
        self._title = title
        self._cnt = cnt

    def __str__(self):
        return str({'id': self._id,
                    'title': self._title,
                    'cnt': self._cnt})

    def asdict(self):
        _dict = OrderedDict()
        table = class_mapper(self.__class__).mapped_table
        for col in table.c:
            val = getattr(self, col.name)
            if isinstance(val, date):
                val = str(val)
            if isinstance(val, datetime):
                val = val.isoformat()
            _dict[col.name] = val
        return _dict
