# -*- coding: utf-8 -*-
import pytest
from app.models import AppUser
import json


@pytest.mark.django_db
def test_user(client):
    url = '/api/user/login/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['code'] == 501
    assert response.json()['message'] == 'Not support this method'

    response = client.post(url)
    assert response.status_code == 200
    assert response.json()['code'] == 402
    assert response.json()['message'] == 'Username and Password not match'

    user = AppUser.objects.create_user(username='test', password='test')
    user.save()

    response = client.post(url, data={'username': 'test', 'password': 'test'})
    assert response.status_code == 200
    response = json.loads(response.json()['message'])
    assert response['username'] == 'test'
    assert response['user_id'] == user.pk
