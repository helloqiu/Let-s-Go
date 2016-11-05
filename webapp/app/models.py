from django.db import models
from django.db.models import CharField, DateField, ManyToManyField, ForeignKey, TextField, DateTimeField, IntegerField
from django.contrib.auth.models import AbstractUser, UserManager


class AppUser(AbstractUser):
    objects = UserManager()
    phone = CharField('phone', max_length=18, blank=True, null=True)
    gender = CharField('gender', max_length=2, blank=True, null=True)
    birthday = DateField('birthday', blank=True, null=True)
    place = ManyToManyField('Place', blank=True)

    def __str__(self):
        return '[%s],id[%d]' % (self.username, self.id)

    class Admin:
        list_display = ('username')

    class Meta:
        ordering = ['username']


class Label(models.Model):
    name = CharField('name', max_length=255, null=False, db_index=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']


class Place(models.Model):
    name = CharField('name', max_length=255, null=False, db_index=True)
    label = ManyToManyField('Label', blank=True)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        ordering = ['name']


class Guide(models.Model):
    name = CharField('name', max_length=255, null=False)
    user = ForeignKey('AppUser', null=False, db_index=True)
    place = ForeignKey('Place', null=False, db_index=True)
    start_time = DateField('start_time', null=False)
    end_time = DateField('end_time', null=False)
    content = TextField('content', null=False)
    submit = DateTimeField('submit', auto_now=True)
    pageview = IntegerField('pageview', default=0, db_index=True)
    praise = IntegerField('praise', default=0, db_index=True)
    label = ManyToManyField('Label', blank=True)

    def __str__(self):
        return '[%s]@%s' % (self.submit, self.user.username)

    class Meta:
        ordering = ['user', 'name', 'place']


class Question(models.Model):
    user = ForeignKey('AppUser', null=False, db_index=True)
    place = ForeignKey('Place', null=False, db_index=True)
    title = CharField('title', max_length=255, null=False)
    content = TextField('content', null=False)
    submit = DateTimeField('submit', auto_now=True)
    label = ManyToManyField('Label', blank=True)

    def __str__(self):
        return '[%s]@%s:%s' % (self.submit, self.user.username, self.title)

    class Meta:
        ordering = ['user', 'title', 'place']


class Wish(models.Model):
    user = ForeignKey('AppUser')
    place = ForeignKey('Place')
    label = ManyToManyField('Label')
    start_time = DateField('start_time', blank=True, null=True)
    end_time = DateField('end_time', blank=True, null=True)
    nums_together = IntegerField('nums_together', null=False, db_index=True)
    message = TextField('message', blank=True, null=True)

    def __str__(self):
        return '@%s:%s' % (self.user.username, self.place.name)

    class Meta:
        ordering = ['user', 'place']


class Special(models.Model):
    user = ForeignKey('AppUser')
    place = ForeignKey('Place')
    start_time = DateField('start_time', blank=True, null=True)
    end_time = DateField('end_time', blank=True, null=True)
    message = TextField('message', blank=True, null=True)
    label = ManyToManyField('Label', blank=True)

    def __str__(self):
        return '@%s:%s' % (self.user.username, self.place.name)

    class Meta:
        ordering = ['user', 'place']
