from django.contrib import admin
from .models import Scoreboard

class Scoreboard_admin(admin.ModelAdmin):
    list_display=['name','score']

admin.site.register(Scoreboard,Scoreboard_admin)