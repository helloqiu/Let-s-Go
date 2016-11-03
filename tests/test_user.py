# -*- coding: utf-8 -*-
import pytest


@pytest.mark.django_db
def test_user(client):
    response = client.post('/api/user/login/')
    assert response.status_code == 200
