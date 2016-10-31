from django.contrib import admin
from app.models import AppUser, Label, Place, Guide, Question


admin.site.register([AppUser, Label, Place, Guide, Question])
# admin.site.register(Label)
# admin.site.register(Place)
# admin.site.register(Visited)
# admin.site.register(Guide)
# admin.site.register(Question)
