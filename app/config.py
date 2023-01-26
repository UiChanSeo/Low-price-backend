import os


class Dev:
    jwt_key = 'dkakehzl'
    db_name = 'goods_dev.db'
    db_url = 'sqlite:///' + db_name


class Prod:
    jwt_key = 'dkakehzl'
    db_name = 'goods-prod.db'
    db_url = 'sqlite:///:' + db_name + ':'


confs = {"prod": Prod, "dev": Dev}

active_conf = confs[os.getenv('RUN', 'dev')]
