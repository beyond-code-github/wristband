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
    app.config.from_envvar("CONFIG_FILE", conf_file)
    app.register_blueprint(main_app)
    app.register_blueprint(
        api_v1_bp,
        url_prefix='/api/v{version}'.format(version=API_VERSION_V1)
    )

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
