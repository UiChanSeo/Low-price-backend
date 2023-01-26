from flask import Blueprint, render_template

main_ctl = Blueprint('main_ctl', __name__, url_prefix='/main')


@main_ctl.route('/', methods=['GET'])
def index():
    return render_template('/main/index.html')


@main_ctl.route('/about', methods=['GET'])
def about():
    return 'Hello Goods V0.1'
