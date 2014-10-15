from django.contrib import admin
from mc.models import Config,Decision
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Config)
admin.site.register(Decision)