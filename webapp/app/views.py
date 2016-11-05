from django.contrib.auth import authenticate, logout
# from django.contrib.auth import get_user_model
from django.http import HttpResponse
import json

LOGIN_OK_CODE = 200
LOGIN_OK = 'Login success'
LOGOUT_OK_CODE = 201
LOGOUT_OK = 'Logout success'
HAD_LOGIN_CODE = 301
HAD_LOGIN = 'Had logined'
NOT_LOGIN_CODE = 301
NOT_LOGIN = 'Not login'
NOT_ACTIVE_CODE = 401
NOT_ACTIVE = 'User Not Active'
NOT_MATCH_CODE = 402
NOT_MATCH = 'Username and Password not match'
INVALIED_CODE = 501
INVALIED = 'Not support this method'


def index(request):
    return HttpResponse("hello.")


def test(request):
    return HttpResponse("test ok")


def JSON(**kwargs):
    return json.dumps(kwargs)


def user_logout(request):
    if request.user.is_authenticated():
        logout(request)
        data = JSON(code=LOGOUT_OK_CODE, status=True, message=LOGOUT_OK)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=True, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def user_login(request):
    if request.user.is_authenticated():
        data = JSON(code=NOT_MATCH_CODE, status=False, message=NOT_MATCH)
        return HttpResponse(data, content_type="application/json")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                message = JSON(user_id=user.id, username=user.username)
                data = JSON(code=LOGIN_OK_CODE, status=True, message=message)
            else:
                data = JSON(code=NOT_ACTIVE_CODE, status=False,
                            message=NOT_ACTIVE)
        else:
            data = JSON(code=NOT_MATCH_CODE, status=False, message=NOT_MATCH)
    else:
        data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)

    return HttpResponse(data, content_type="application/json")
