from arcnet.core.models import *
from django.contrib import admin

class ComputerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
                'fields': ('name','address','security_level','description','auto_ice','ice'),
                }),
        )
#    readonly_fields = ('ice',)


class ICEAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
                'fields': ('ice_type','level','seed'),
                }),
        )
    readonly_fields = ('seed',)

admin.site.register(Computer, ComputerAdmin)
admin.site.register(ICE, ICEAdmin)

admin.site.register(Access)
admin.site.register(Rumor)
admin.site.register(Trance)
admin.site.register(Word)
admin.site.register(Picture)
