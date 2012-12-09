from arcnet.core.models import *
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
#admin.site.register(Character,UserAdmin)

admin.site.register(Character)
admin.site.register(Permission)



