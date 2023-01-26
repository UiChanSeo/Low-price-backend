from flask import Blueprint
from flask import request
from flask import jsonify
from flask_login import login_user, logout_user, current_user
from app.model.users import User
from app.service.user_service import UserService

loginout_ctl = Blueprint('loginout_ctl', __name__, url_prefix='/auth')


@loginout_ctl.route("/user/add", methods=['POST'])
def add_user():
    userid = request.json['userid']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    ret = UserService.add(userid, username, email, password)
    if not ret:
        res = {'ok': False, 'error': 'user <%s> already exists' % userid}
    else:
        res = {'ok': True, 'msg': 'user <%s> added' % userid}
    return jsonify(res)


@loginout_ctl.route("/user/get/<userid>", methods=['POST'])
def get_user(userid):
    ret, user = UserService.get(userid)
    if not ret:
        json_res = {'ok': False, 'error': 'user <%s> does not exist' % userid}
    else:
        json_res = {'ok': True, 'info': '<%s>' % str(user)}
    return jsonify(json_res)


@loginout_ctl.route("/user/get", methods=['POST'])
def get_user_all():
    ret, user = UserService.get()
    if not ret:
        json_res = {'ok': False, 'error': f'user {user.userid} does not exist'}
    else:
        json_res = {'ok': True, 'info': f'<{user}>'}
    return jsonify(json_res)


@loginout_ctl.route("/user/del/<userid>", methods=['POST'])
def del_user(userid: str):
    ret = UserService.delete(userid)
    if not ret:
        json_res = {'ok': False, 'error': 'user <%s> does not exist' % userid}
    else:
        json_res = {'ok': True, 'msg': 'user <%s> is deleted' % userid}
    return jsonify(json_res)


def create_jwt_token(user: User, user_passwd: str) -> str:
    print(f'create_jwt_token : user={type(user)}')
    new_jwt_token = user.login(user_passwd)
    print(f'refresh_jwt_token : type={type(new_jwt_token)}')
    try:
        if new_jwt_token is not None:
            user.authenticated = False
            user.token = new_jwt_token.decode('utf8')
            UserService.update_token(user.userid, new_jwt_token.decode('utf8'))
            login_user(user, remember=True)
            json_res = {'ok': True,
                        'msg': 'user <%s> refreshed' % user.userid,
                        'token': new_jwt_token.decode('utf8')}
        else:
            json_res = {'ok': False, 'error': 'Error : can\'t create token'}
    except:
        json_res = {'ok': False, 'error': "Error : can\'t refresh token"}
    return json_res


@loginout_ctl.route('/login', methods=['POST'])
def login():
    userid = request.json['userid']
    user_passwd = request.json['password']

    if 'token' in request.json:
        login_token = request.json['token']
    else:
        login_token = None

    try:
        if login_token is None:
            ret, user = UserService.get(userid, True)
            if not ret:
                json_res = {'ok': False, 'error': 'Error : not found user'}
            else:
                json_res = create_jwt_token(user[0], user_passwd)
        else:
            result, userid_sub = User.decode_auth_token(login_token)
            if result:
                json_res = {'ok': True, 'msg': 'user <%s> logined' % userid_sub}
            else:
                json_res = {'ok': False, 'msg': 'user <%s> invalid token' % userid}
    except Exception as e:
        json_res = {'ok': False, 'msg': e}
    print(f'{json_res}')
    return jsonify(json_res)


@loginout_ctl.route('/logout', methods=['POST'])
def logout():
    user = current_user
    user.authenticated = False
    print(f'logout => userid={user.userid}, token={user.token}')
    user.token = ''
    json_res = {'ok': True, 'msg': 'user <%s> logout' % user.userid}
    logout_user()
    print(f'{json_res}')
    return jsonify(json_res)
