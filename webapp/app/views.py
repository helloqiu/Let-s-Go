from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from app.models import Label, Place, Guide, Question, Answer
from hashlib import md5
import json
import re


LOGIN_OK_CODE = 200
LOGIN_OK = 'Login success'
LOGOUT_OK_CODE = 201
LOGOUT_OK = 'Logout success'
REG_OK_CODE = 202
REG_OK = 'Regist success'
QUERY_OK_CODE = 203
QUERY_OK = ''
ADD_OK_CODE = 203
ADD_OK = 'Add success'
GET_OK_CODE = 204
GET_OK = ''
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
NAME_EX_CODE = 424
NAME_EX = 'This name is already exists'
KEY_ERR_CODE = 425
KEY_ERR = 'The Key Error'
ID_ERR_CODE = 426
ID_ERR = 'The ID Error'
TITLE_ERR_CODE = 427
TITLE_ERR = 'The Title Error'
PLACE_ERR_CODE = 428
PLACE_ERR = 'The Place Error'
LABEL_ERR_CODE = 429
LABEL_ERR = 'The Label Error'
NAME_ERR_CODE = 430
NAME_ERR = 'Name Error'
NAME_NEX_CODE = 431
NAME_NEX = 'Name Not exists'
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
                    birthday = birthday.replace('.', '-').replace('/', '-')
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


def guide_add(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            place = request.POST.get('place')
            label = request.POST.getlist('label[]')
            start_time = request.POST.get('start_time')
            end_time = request.POST.get('end_time')

            if len(title) == 0:
                data = JSON(code=TITLE_ERR_CODE, status=False,
                            message=TITLE_ERR)
            elif len(place) == 0:
                data = JSON(code=PLACE_ERR_CODE, status=False,
                            message=PLACE_ERR)
            elif re.match(r'(\d{4}([-/\.])\d{2}\2\d{2})', start_time) is None:
                data = JSON(code=DATE_ERR_CODE, status=False, message=DATE_ERR)
            elif re.match(r'(\d{4}([-/\.])\d{2}\2\d{2})', end_time) is None:
                data = JSON(code=DATE_ERR_CODE, status=False, message=DATE_ERR)
            elif start_time > end_time:
                data = JSON(code=DATE_ERR_CODE, status=False, message=DATE_ERR)
            elif not Place.objects.filter(id=place):
                data = JSON(code=PLACE_ERR_CODE, status=False,
                            message=PLACE_ERR)
            else:
                label = Label.objects.filter(id__in=label)
                a = Guide(name=title, user=request.user,
                          place=Place.objects.get(id=place), content=content,
                          start_time=start_time, end_time=end_time)
                a.save()
                a.label.add(*label)
                data = JSON(code=ADD_OK_CODE, status=True, message=ADD_OK)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def guide_id(request, _id):
    if request.user.is_authenticated():
        try:
            guide = Guide.objects.filter(id=_id)[0]
            labels = []
            for l in guide.label.all():
                labels.append(l.name)
            submit = str(guide.submit.strftime('%Y-%m-%d %H:%M:%S'))
            result = {'title': guide.name, 'username': guide.user.username,
                      'place': guide.place.name, 'labels': labels,
                      'start_time': str(guide.start_time),
                      'end_time': str(guide.end_time),
                      'content': guide.content, 'submit': submit,
                      'pageview': guide.pageview}
            guide.pageview += 1
            guide.save()
            data = JSON(code=GET_OK_CODE, status=True, message=result)
        except IndexError:
            data = JSON(code=ID_ERR_CODE, status=False, message=ID_ERR)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def guide_list(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            start = int(request.POST.get('start'))
            offset = int(request.POST.get('offset'))
            try:
                ans = Guide.objects.order_by('-id')[start:start + offset]
            except IndexError:
                ans = []
            result = []
            for i in ans:
                labels = []
                for l in i.label.all():
                    labels.append(l.name)
                m = md5()
                m.update(i.user.email.encode())
                img = 'http://gravatar.eqoe.cn/avatar/%s?size=48&default=identicon&rating=pg' % (m.hexdigest())
                _ = {'id': i.id, 'username': i.user.username, 'title': i.name,
                     'place': i.place.name, 'pageview': i.pageview,
                     'labels': labels, 'img': img}
                result.append(_)
            data = JSON(code=QUERY_OK_CODE, status=True, message=result)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def question_add(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            place = request.POST.get('place')
            label = request.POST.getlist('label[]')

            if len(title) == 0:
                data = JSON(code=TITLE_ERR_CODE, status=False,
                            message=TITLE_ERR)
            elif len(place) == 0:
                data = JSON(code=PLACE_ERR_CODE, status=False,
                            message=PLACE_ERR)
            elif not Place.objects.filter(id=place):
                data = JSON(code=PLACE_ERR_CODE, status=False,
                            message=PLACE_ERR)
            else:
                label = Label.objects.filter(id__in=label)
                a = Question(title=title, user=request.user,
                             place=Place.objects.get(id=place),
                             content=content)
                a.save()
                a.label.add(*label)
                data = JSON(code=ADD_OK_CODE, status=True, message=ADD_OK)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def question_id(request, _id):
    if request.user.is_authenticated():
        try:
            question = Question.objects.filter(id=_id)[0]
            labels = []
            for l in question.label.all():
                labels.append(l.name)

            answers = []
            for i in Answer.objects.filter(question=question).order_by('-submit'):
                m = md5()
                m.update(i.user.email.encode())
                img = 'http://gravatar.eqoe.cn/avatar/%s?size=48&default=identicon&rating=pg' % (m.hexdigest())
                _submit = str(i.submit.strftime('%Y-%m-%d %H:%M:%S'))
                _ = {'id': i.id, 'username': i.user.username, 'img': img,
                     'content': i.content, 'submit': _submit}
                answers.append(_)
            submit = str(question.submit.strftime('%Y-%m-%d %H:%M:%S'))
            result = {'title': question.title,
                      'username': question.user.username,
                      'place': question.place.name, 'labels': labels,
                      'content': question.content, 'submit': submit,
                      'answer': answers}
            data = JSON(code=GET_OK_CODE, status=True, message=result)
        except IndexError:
            data = JSON(code=ID_ERR_CODE, status=False, message=ID_ERR)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def question_comment(request, _id):
    if request.user.is_authenticated():
        if request.method == 'POST':
            content = request.POST.get('content')
        try:
            question = Question.objects.filter(id=_id)[0]
            answer = Answer(user=request.user, question=question,
                            content=content)
            answer.save()
            data = JSON(code=ADD_OK_CODE, status=True, message=ADD_OK)
        except IndexError:
            data = JSON(code=ID_ERR_CODE, status=False, message=ID_ERR)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def question_list(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            start = int(request.POST.get('start'))
            offset = int(request.POST.get('offset'))
            try:
                ans = Question.objects.order_by('-id')[start:start + offset]
            except IndexError:
                ans = []
            result = []
            for i in ans:
                labels = []
                for l in i.label.all():
                    labels.append(l.name)
                m = md5()
                m.update(i.user.email.encode())
                ans_count = len(Answer.objects.filter(question=i))
                img = 'http://gravatar.eqoe.cn/avatar/%s?size=48&default=identicon&rating=pg' % (m.hexdigest())
                _ = {'id': i.id, 'username': i.user.username, 'title': i.title,
                     'place': i.place.name, 'answer': ans_count,
                     'labels': labels, 'img': img}
                result.append(_)
            data = JSON(code=QUERY_OK_CODE, status=True, message=result)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def __id(request, _id, model):
    if request.user.is_authenticated():
        try:
            ans = model.objects.filter(id=_id)[0].name
            data = JSON(code=QUERY_OK_CODE, status=True, message=ans)
        except IndexError:
            data = JSON(code=ID_ERR_CODE, status=False, message=ID_ERR)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def label_id(request, _id):
    return __id(request, _id, Label)


def place_id(request, _id):
    return __id(request, _id, Place)


def __list(request, model):
    if request.user.is_authenticated():
        ans = list(model.objects.values('id', 'name'))
        data = JSON(code=QUERY_OK_CODE, status=True, message=ans)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def place_list(request):
    return __list(request, Place)


def label_list(request):
    return __list(request, Label)


def user_add_place(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if 'name' in request.POST:
                name = request.POST.get('name')
                if len(name) == 0:
                    data = data = JSON(code=NAME_ERR_CODE, status=True,
                                       message=NAME_ERR)
                elif not Place.objects.filter(name=name):
                    data = JSON(code=NAME_NEX_CODE, status=False,
                                message=NAME_NEX)
                else:
                    request.user.place.add(Place.objects.get(name=name))
                    data = JSON(code=ADD_OK_CODE, status=True, message=ADD_OK)
            else:
                data = JSON(code=KEY_ERR_CODE, status=False, message=KEY_ERR)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def __add(request, model):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if 'name' in request.POST:
                name = request.POST.get('name')

                if len(name) == 0:
                    data = data = JSON(code=NAME_ERR_CODE, status=True,
                                       message=NAME_ERR)
                elif model.objects.filter(name=name):
                    data = JSON(code=NAME_EX_CODE, status=False,
                                message=NAME_EX)
                else:
                    add = model(name=name)
                    add.save()
                    data = JSON(code=ADD_OK_CODE, status=True, message=ADD_OK)
            else:
                data = JSON(code=KEY_ERR_CODE, status=False, message=KEY_ERR)
        else:
            data = JSON(code=INVALIED_CODE, status=False, message=INVALIED)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")


def label_add(request):
    return __add(request, Label)


def place_add(request):
    return __add(request, Place)


def user_info(request):
    if request.user.is_authenticated():
        I = request.user
        places = []
        for l in I.place.all():
            places.append(l.name)
        result = {'username': I.username, 'id': I.id,
                  'places': places, 'birthday': str(I.birthday),
                  'gender': I.gender}
        data = JSON(code=GET_OK_CODE, status=True, message=result)
    else:
        data = JSON(code=NOT_LOGIN_CODE, status=False, message=NOT_LOGIN)
    return HttpResponse(data, content_type="application/json")
