from app.model.goods import Goods
from app.service.goods_info_db import DatabaseFactory
from datetime import datetime


class GoodsService:

    @classmethod
    def get(cls,
            name: str = None,
            category_id: int = -1,
            sel_limit: int = 10):
        """
        get goods

        :param name: str, goods name
        :param category_id: int, id of category
        :param sel_limit: int, not used..
        """

        goods_list = []
        if name is not None:
            goods_list = DatabaseFactory.session.query(Goods).all()
        else:
            goods = DatabaseFactory.session.query(Goods).filter(name=Goods._name).first()
            goods_list.append(goods)
        return len(goods_list), goods_list

    @classmethod
    def delete(cls, name: str = None, category_id: int = -1, mall_name: str = None):
        """
        delete goods

        :param name: str, goods name
        :param category_id: int, id of category
        :param mall_name: str, name of mall
        """

        session = DatabaseFactory.session
        if name is not None:
            goods = session.query(Goods).filter(name == Goods._name).all()

            if goods is not None and len(goods) > 0:
                session.query(Goods).filter(name == Goods._name).delete()

        else:
            session.query(Goods).delete()

        session.flush()
        session.commit()

    @classmethod
    def add(cls, goods: Goods):
        """
        add goods

        :param goods: Goods, goods info
        """

        session = DatabaseFactory.session
        goods._id = None

        goods1 = session.query(Goods).filter(Goods._name == goods.name).first()
        if goods1 is None:
            session.add(Goods(goods.name, goods.category_id, goods.goods_url, goods.image_url, goods.mall_name, goods.lprice, goods.hprice, goods.cnt))
        else:
            goods1._lprice = goods.lprice
            goods1._hprice = goods.hprice
            goods1._updated = datetime.now()

        session.flush()
        session.commit()
