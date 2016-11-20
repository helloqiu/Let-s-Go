from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import json
import re


LOGIN_OK_CODE = 200
LOGIN_OK = 'Login success'
LOGOUT_OK_CODE = 201
LOGOUT_OK = 'Logout success'
REG_OK_CODE = 202
REG_OK = 'Regist success'
HAD_LOGIN_CODE = 301
HAD_LOGIN = 'Had logined'
NOT_LOGIN_CODE = 301
NOT_LOGIN = 'Not login'
NOT_ACTIVE_CODE = 401
NOT_ACTIVE = 'User Not Active'
NOT_MATCH_CODE = 402
NOT_MATCH = 'Username and Password not match'
DATE_ERR_CODE = 411
DATE_ERR = 'Datetime is not allow'
GENDER_ERR_CODE = 412
GENDER_ERR = 'Gender is not allow'
PHONE_ERR_CODE = 413
PHONE_ERR = 'Phone num is not allow'
EMAIL_ERR_CODE = 414
EMAIL_ERR = 'Email is not allow'
PHONE_EX_CODE = 421
PHONE_EX = 'Phone has already regist'
EMAIL_EX_CODE = 422
EMAIL_EX = 'Email has already regist'
UNAME_EX_CODE = 423
UNAME_EX = 'Username has already regist'
INVALIED_CODE = 501
INVALIED = 'Not support this method'
UN_ERROR_CODE = 502
UN_ERROR = 'Something error'


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
        data = JSON(code=HAD_LOGIN_CODE, status=True, message=HAD_LOGIN)
        return HttpResponse(data, content_type="application/json")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                message = JSON(user_id=user.id, username=user.username)
                data = JSON(code=LOGIN_OK_CODE, status=True, message=message)
                login(request, user)
            else:
                data = JSON(code=NOT_ACTIVE_CODE, status=False,
                            message=NOT_ACTIVE)
        else:
            data = JSON(code=NOT_MATCH_CODE, status=False, message=NOT_MATCH)
    else:
        data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)

    return HttpResponse(data, content_type="application/json")


def user_register(request):
    if request.user.is_authenticated():
        data = JSON(code=HAD_LOGIN_CODE, status=False, message=HAD_LOGIN)
    elif not request.method == 'POST':
        data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        # check format
        if re.match(r'(\d{4}([-/\.])\d{2}\2\d{2})', birthday) is None:
            data = JSON(code=DATE_ERR_CODE, status=False, message=DATE_ERR)
        elif gender not in {'1', '0'}:
            data = JSON(code=GENDER_ERR_CODE, status=False, message=GENDER_ERR)
        elif re.match(r'(\+\d{1,3})?1\d{10}', phone) is None:
            data = JSON(code=PHONE_ERR_CODE, status=False, message=PHONE_ERR)
        elif re.match(r'[^@\s]+@([^@\s]+\.)+[^@\s]+', email) is None:
            data = JSON(code=EMAIL_ERR_CODE, status=False, message=EMAIL_ERR)
        # database search
        else:
            all_user = get_user_model().objects
            if all_user.filter(phone=phone).count() != 0:
                data = JSON(CODE=PHONE_EX_CODE, status=False, message=PHONE_EX)
            elif all_user.filter(email=email).count() != 0:
                data = JSON(CODE=EMAIL_EX_CODE, status=False, message=EMAIL_EX)
            elif all_user.filter(username=username).count() != 0:
                data = JSON(CODE=UNAME_EX_CODE, status=False, message=UNAME_EX)
            else:

                app_user = get_user_model()
                try:
                    user = app_user.objects.create_user(username=username,
                                                        password=password,
                                                        email=email,
                                                        phone=phone,
                                                        gender=gender,
                                                        birthday=birthday)
                    message = JSON(user_id=user.id, username=user.username)
                    data = JSON(code=REG_OK_CODE, status=True, message=message)
                except Exception as e:
                    print(e)
                    data = JSON(code=UN_ERROR_CODE, status=False,
                                message=UN_ERROR)
    return HttpResponse(data, content_type="application/json")
