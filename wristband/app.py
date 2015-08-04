import os

from flask import Flask, jsonify, Blueprint, session, request, Response

from api.v1 import api_v1_bp, API_VERSION_V1
from auth import ldap_authentication

main_app = Blueprint('main_app', __name__)


@main_app.route('/ping/ping')
def ping():
    return Response(jsonify({'status': 'OK'}))


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
        return Response(jsonify({'status': 'OK'}))
    else:
        return Response('Unauthorised', 401)


@main_app.route('/logout', methods=['GET'])
def logout():
    try:
        del session['authenticated']
    except KeyError:
        # not authenticated, do nothing
        pass
    return Response(jsonify({'status': 'OK'}))



def create_app(conf_file=None):
    conf_file = conf_file or 'config/production.py'
    app = Flask(__name__)
    app.secret_key = 'not_so_secret_key'
    app.config.from_envvar("CONFIG_FILE", conf_file)
    # blueprint registration
    app.register_blueprint(main_app)
    app.register_blueprint(
        api_v1_bp,
        url_prefix='/api/v{version}'.format(version=API_VERSION_V1)
    )
    return app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
