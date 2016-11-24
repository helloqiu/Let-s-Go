from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'test/$', views.test),
    url(r'user/login/$', views.user_login),
    url(r'user/logout/$', views.user_logout),
    url(r'user/register/$', views.user_register),
    url(r'label/list/$', views.label_list),
    url(r'label/add/$', views.label_add),
    url(r'label/(\d{1,})/$', views.label_id),
    url(r'place/list/$', views.place_list),
    url(r'place/add/$', views.place_add),
    url(r'place/(\d{1,})/$', views.place_id),
    url(r'guide/list/$', views.guide_list),
    url(r'guide/add/$', views.guide_add),
    url(r'guide/(\d{1,})/$', views.guide_id),
    url(r'question/list/$', views.question_list),
    url(r'question/add/$', views.question_add),
    url(r'question/(\d{1,})/$', views.question_id),
    url(r'user/info/$', views.user_info),
    url(r'user/place/$', views.user_add_place),
    url(r'question/(\d{1,})/comment/$', views.question_comment),
]
