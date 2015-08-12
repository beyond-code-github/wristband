import os

from flask import Flask, jsonify, Blueprint

from api.v1 import api_v1_bp, API_VERSION_V1

main_app = Blueprint('main_app', __name__)


@main_app.route('/ping/ping')
def ping():
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
    app.authentication_enabled = os.getenv('AUTH', True)
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
