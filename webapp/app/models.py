from django.db import models
from django.db.models import CharField, DateField, ManyToManyField, ForeignKey, TextField, DateTimeField, IntegerField
from django.contrib.auth.models import AbstractUser, UserManager


class AppUser(AbstractUser):
    objects = UserManager()
    phone = CharField('phone', max_length=18, null=False)
    gender = CharField('gender', max_length=2, null=True, db_index=True)
    birthday = DateField('birthday', null=True)
    place = ManyToManyField('Place')


class Label(models.Model):
    name = CharField('name', max_length=255, null=False, db_index=True)


class Place(models.Model):
    name = CharField('name', max_length=255, null=False, db_index=True)
    label = ManyToManyField('Label')


# class Visited(models.Model):
#     user = ForeignKey('AppUser', null=False, db_index=True)
#     place = ForeignKey('Place', null=False, db_index=True)


# class place_label():
#     place = ForeignKey(place, null=False, db_index=True)
#     label_name = CharField('label_name', null=True, , db_index=True)


class Guide(models.Model):
    name = CharField('name', max_length=255, null=False)
    user = ForeignKey('AppUser', null=False, db_index=True)
    place = ForeignKey('Place', null=False, db_index=True)
    start_time = DateField('start_tile', null=False)
    end_time = DateField('end_tile', null=False)
    content = TextField('content', null=False)
    submit = DateTimeField('submit', auto_now=True)
    pageview = IntegerField('pageview', default=0, db_index=True)
    praise = IntegerField('praise', default=0, db_index=True)
    label = ManyToManyField('Label')


# class guide_label():
#     guide = ForeignKey(guide, null=False, db_index=True)
#     label_name = CharField('label_name', null=True, , db_index=True)


class Question(models.Model):
    user = ForeignKey('AppUser', null=False, db_index=True)
    place = ForeignKey('Place', null=False, db_index=True)
    content = TextField('content', null=False)
    submit = DateTimeField('submit', auto_now=True)
    label = ManyToManyField('Label')


# class question_label():
#     question = ForeignKey(question, null=False, db_index=True)
#     label_name = CharField('label_name', null=True, , db_index=True)
