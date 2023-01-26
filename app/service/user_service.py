from app.model.users import User
from app.service.goods_info_db import DatabaseFactory


class UserService:

    @classmethod
    def get(cls, userid: str = None, get_val: bool = True) -> (bool, []):

        """
        get_user

        :param userid: string, userid to get
        :param get_val: bool, flag means you will do get data or don't
        """

        print(f'get, userid={userid}, get_val={get_val}')

        session = DatabaseFactory.session
        users = []

        if userid is not None:
            user = session.query(User).filter(userid == User._userid).first()
            users.append(user)
        else:
            u_list = session.query(User).all()
            users.extend(u_list)

        print(f'get = {users}')

        if users is not None:
            if get_val is True:
                return True, users
            else:
                return True, None

        return False, None

    @classmethod
    def add(cls,
            userid: str,
            username: str,
            email: str,
            password: str) -> (bool, str):

        """
        add user

        :param userid: string, userid
        :param username: string, username
        :param email: string, email
        :param password: string, user password
        """

        try:
            ret, user = cls.get(userid, False)
            print(f'add = {user}')
            if not ret:
                session = DatabaseFactory.session
                user = User(userid=userid,
                            username=username,
                            email=email,
                            password=password)
                session.add(user)
                session.flush()
                session.commit()

                return True, 'success'
            return False, 'existed user'
        except Exception as e:
            return False, str(e)

    @classmethod
    def delete(cls, userid: str):

        """
        del_user

        :param userid: string, userid to delete
        """

        ret, user = cls.get(userid, False)

        if ret:
            session = DatabaseFactory.session
            session.query(User).filter(userid == User.userid).delete()
            return True

        return False

    @classmethod
    def update_token(cls, userid: str, token: str):

        """
        update_token 

        :param userid: string, userid for updating
        :param token: string, new token value
        """

        print('update_token', userid, token)
        ret, user = cls.get(userid, True)

        if user is not None:
            session = DatabaseFactory.session
            user[0]._token = token
            session.flush()
            session.commit()
            return True

        return False
