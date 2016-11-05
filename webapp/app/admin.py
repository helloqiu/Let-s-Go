from django.contrib import admin
from app.models import AppUser, Label, Place, Guide, Question, Wish, Special


admin.site.register([AppUser, Label, Place, Guide, Question, Wish, Special])
