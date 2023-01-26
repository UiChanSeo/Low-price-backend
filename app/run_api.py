import os
from app.config import active_conf


def create_app(name: str):
    from flask import Flask
    # from flask_login import LoginManager
    import flask_login

    flask_app = Flask(__name__)

    from app.service.goods_info_db import DatabaseFactory

    DatabaseFactory.initialize(flask_app)

    flask_app.secret_key = os.urandom(24)
    flask_app.config['JWT_SECRET_KEY'] = active_conf.jwt_key

    from app.controller.main_ctl import main_ctl
    from app.controller.goods_ctl import goods_ctl
    from app.controller.category_ctl import category_ctl
    from app.controller.loginout_ctl import loginout_ctl

    flask_app.register_blueprint(category_ctl)
    flask_app.register_blueprint(goods_ctl)
    flask_app.register_blueprint(main_ctl)
    flask_app.register_blueprint(loginout_ctl)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(flask_app)

    from app.service.user_service import UserService
    from app.model.users import User

    @login_manager.user_loader
    def user_loader(user_id) -> User:
        ret, user = UserService.get(user_id)
        return user[0]

    return flask_app


app = create_app(__name__)

if __name__ == "__main__":
    app.run(host='0.0.0.0',
            debug=True,
            threaded=True)
