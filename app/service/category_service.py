from app.model.category import Category
from app.service.goods_info_db import DatabaseFactory


class CategoryService():
    @classmethod
    def inc_cnt(cls, title: str) -> (bool, int):

        session = DatabaseFactory.session
        category = session.query(Category).filter(
            title == Category.title).first()

        if category is not None:
            category._cnt += 1

            session.flush()
            session.commit()
            return True, category._cnt
        return False, -1

    @classmethod
    def delete(cls, title: str = None):
        session = DatabaseFactory.session
        if title != None:
            cat = session.query(Category).filter(title == Category._title).first()
            if cat is not None:
                session.query(Category).filter(title == Category._title).delete()
                session.flush()
                session.commit()
        else:
            session.query(Category).delete()
            session.flush()
            session.commit()

    @classmethod
    def add(cls, title: str) -> bool:
        try:
            session = DatabaseFactory.session
            cat = session.query(Category).filter(title == Category._title).first()
            if cat is None:
                category = Category(title=title)
                session.add(category)
                session.flush()
                session.commit()
            return True
        except Exception as e:
            print('Exception', e)
        return False

    @classmethod
    def get(cls, title: str = None) -> []:

        session = DatabaseFactory.session

        if title is None:
            return session.query(Category).all()

        categories = [session.query(Category).filter(title == Category._title).first()]

        print(__name__, 'get', categories)

        return categories
