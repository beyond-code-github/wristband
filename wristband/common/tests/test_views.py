from django.http import HttpResponse
from django.shortcuts import resolve_url

def test_healthcheck_view(client):
    url = resolve_url('healthcheck')
    response = client.get(url)
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200
    assert response.content == ''
