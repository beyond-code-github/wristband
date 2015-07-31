import json
from flask import url_for

def test_ping(client):
    url = url_for('main_app.ping')
    resource = client.get(url)
    assert json.loads(resource.data) == {'status': 'OK'}
