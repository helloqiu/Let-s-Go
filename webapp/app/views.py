from django.contrib.auth import authenticate, logout
# from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
import json


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
    logout(request)
    return HttpResponseRedirect('/')


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponse('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = JSON(user_id=user.id, username=user.username)
            else:
                data = JSON(code=NOT_ACTIVE_CODE, status=False,
                            message=NOT_ACTIVE)
        else:
            data = JSON(code=NOT_MATCH_CODE, status=False, message=NOT_MATCH)
    else:
        data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    return HttpResponse(data, content_type="application/json")
