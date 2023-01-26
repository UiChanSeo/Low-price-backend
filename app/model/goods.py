import datetime
from datetime import datetime, date
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql.sqltypes import DateTime
from app.model import Base
from collections import OrderedDict


class Goods(Base):
    __tablename__ = 'goods'

    # Columns
    _id = Column('id', Integer, primary_key=True)
    _name = Column('name', String)
    _category_id = Column('category_id', Integer)
    _goods_url = Column('goods_url', String)
    _image_url = Column('image_url', String)
    _mall_name = Column('mall_name', String)
    _lprice = Column('lprice', Integer)
    _hprice = Column('hprice', Integer)
    _cnt = Column('cnt', Integer)
    _updated = Column('updated', DateTime)
    _created = Column('created', DateTime)

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category_id(self) -> str:
        return str(self._category_id)

    @property
    def goods_url(self) -> str:
        return self._goods_url

    @property
    def image_url(self) -> str:
        return self._image_url

    @property
    def mall_name(self) -> str:
        return self._mall_name

    @property
    def lprice(self) -> int:
        return self._lprice

    @property
    def hprice(self) -> int:
        return self._hprice

    @property
    def cnt(self) -> int:
        return self._cnt

    @property
    def updated(self) -> datetime:
        return self._updated

    @property
    def created(self) -> datetime:
        return self._created

    def __init__(self,
                 name: str,
                 category_id: int,
                 goods_url: str,
                 image_url: str,
                 mall_name: str,
                 lprice: int,
                 hprice: int,
                 cnt: int):
        self._id = 0
        self._name = name
        self._category_id = category_id
        self._goods_url = goods_url
        self._image_url = image_url
        self._mall_name = mall_name
        self._lprice = lprice
        self._hprice = hprice
        self._cnt = 1
        self._updated = datetime.now()
        self._created = datetime.now()

    def __str__(self):
        return str({'id': self._id,
                    'name': self._name,
                    'category_id': self._category_id,
                    'goods_url': self._goods_url,
                    'image_url': self._image_url,
                    'mall_name': self._mall_name,
                    'hprice': self._hprice,
                    'lprice': self._lprice,
                    'cnt': self._cnt,
                    'updated': self._updated,
                    'created': self._created})

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
