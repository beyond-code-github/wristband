import os

from flask import Flask, jsonify

from api.v1 import api_v1_bp, API_VERSION_V1


def create_app():
    app = Flask(__name__)
    app.config.from_envvar("CONFIG_FILE", "config/production.py")
    app.register_blueprint(
        api_v1_bp,
        url_prefix='/api/v{version}'.format(version=API_VERSION_V1)
    )

    return app

app = create_app()

@app.route('/ping')
def ping():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
