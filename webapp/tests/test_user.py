# -*- coding: utf-8 -*-
import pytest
from app.models import AppUser
import json


@pytest.mark.django_db
def test_user_login(client):
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


@pytest.mark.django_db
def test_user_register(client):
    url = '/api/user/register/'
    response = client.get(url)
    assert response.status_code == 200
    assert response.json()['code'] == 501
    assert response.json()['message'] == 'Not support this method'

    user = dict(username='test_register',
                password='test',
                email='test@test.com',
                phone='13400000000',
                gender='0',
                birthday='2000.01.01')

    user['birthday'] = 'error'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 411
    assert response.json()['message'] == 'Datetime is not allow'
    user['birthday'] = '2000.01.01'

    user['gender'] = 'error'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 412
    assert response.json()['message'] == 'Gender is not allow'
    user['gender'] = '0'

    user['phone'] = 'error'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 413
    assert response.json()['message'] == 'Phone num is not allow'
    user['phone'] = '13400000000'

    user['email'] = 'error'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 414
    assert response.json()['message'] == 'Email is not allow'
    user['email'] = 'test@test.com'

    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 202
    assert json.loads(response.json()['message'])['username'] == 'test_register'

    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 421
    assert response.json()['message'] == 'Phone has already regist'

    user['phone'] = '13400000001'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 422
    assert response.json()['message'] == 'Email has already regist'

    user['email'] = 'test@diff.com'
    response = client.post(url, user)
    assert response.status_code == 200
    assert response.json()['code'] == 423
    assert response.json()['message'] == 'Username has already regist'
