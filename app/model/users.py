import jwt
from datetime import datetime, date, timedelta
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import class_mapper
from sqlalchemy.sql.sqltypes import DateTime
from collections import OrderedDict
from app.model import Base


class User(Base):
    __tablename__ = 'user'

    # Columns
    _id = Column("id", Integer, primary_key=True)
    _userid = Column("userid", String)
    _username = Column("username", String)
    _email = Column("email", String)
    _password = Column("password", String)
    _created = Column("created", DateTime)

    def __init__(self,
                 userid: str,
                 username: str = None,
                 email: str = None,
                 password: str = None,
                 token: str = ''):
        self._userid = userid
        self._username = username
        self._email = email
        self._password = password
        self._created = datetime.now()
        self._token = token

    @property
    def id(self):
        return self._id

    @property
    def created(self) -> DateTime:
        return self._created

    @property
    def userid(self) -> str:
        return self._userid

    @userid.setter
    def userid(self, userid: str):
        self._userid = userid

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = username

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, email: str):
        self._email = email

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = password

    @property
    def token(self) -> str:
        return self._token

    @token.setter
    def token(self, token: str):
        self._token = token

    def is_active(self):
        return True

    def __repr__(self):
        r = {
            'userid': self._userid,
            'username': self._username,
            'email': self._email,
            'password': self._password,
            'created': self._created,
        }
        return str(r)

    def can_login(self, password):
        return self._password == password

    def get_id(self):
        return self._userid

    def is_authenticated(self) -> bool:
        return True

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self._password, password)

    def encode_auth_token(self, userid=None) -> bytes:
        """
        Generates the Auth Token
        :return: string
        """

        if userid is None:
            userid = self._userid

        try:
            payload = {
                'exp': datetime.utcnow() + \
                       timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': userid
            }
            from app.config import active_conf
            return jwt.encode(
                payload,
                active_conf.jwt_key,
                algorithm='HS256'
            )
        except Exception as e:
            print('Exception', e)

        return None

    def login(self, user_pwd: str) -> str:
        if self._password == user_pwd:
            return self.encode_auth_token()
        return None

    @staticmethod
    def decode_auth_token(auth_token) -> (bool, str):
        try:
            from app.config import active_conf
            payload = jwt.decode(auth_token, active_conf.jwt_key)
            return True, payload['sub']
        except jwt.ExpiredSignatureError:
            return False, 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return False, 'Invalid token. Please log in again.'

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


USERS = {
    "user01": User("user01", password='user_01'),
    "user02": User("user02", password='user_02'),
    "user03": User("user03", password='user_03'),
    "simpson": User("simpson", password='12345678'),
}
