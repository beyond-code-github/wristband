import os

from flask import Flask, jsonify, Blueprint, session, request

from api.v1 import api_v1_bp, API_VERSION_V1
from auth import ldap_authentication

main_app = Blueprint('main_app', __name__)


@main_app.route('/ping/ping')
def ping():
    return jsonify({'status': 'OK'})


@main_app.route('/login', methods=['POST'])
def login():
    """
    Ty to authenticate against LDAP, if successful drop a cookie to remember the user session
    """
    username = request.form['username']
    password = request.form['password']
    user = ldap_authentication(username, password)
    if user:
        session['authenticated'] = True
        session['username'] = username
        return jsonify({'status': 'Authorised'})
    else:
        return jsonify({'status': 'Unauthorised'}), 401


@main_app.route('/logout', methods=['GET'])
def logout():
    try:
        del session['authenticated']
        del session['username']
    except KeyError:
        # not authenticated, do nothing
        pass
    return jsonify({'status': 'OK'})


def create_app(conf_file=None):
    conf_file = conf_file or 'config/production.py'
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', 'not_so_secret_key')
    app.config.from_envvar('CONFIG_FILE', conf_file)
    # blueprint registration
    app.register_blueprint(main_app)
    app.register_blueprint(
        api_v1_bp,
        url_prefix='/api/v{version}'.format(version=API_VERSION_V1)
    )
    # make sure we don't accidentally enable any of the testing features
    app.testing = False
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv('PORT', '5000')))
