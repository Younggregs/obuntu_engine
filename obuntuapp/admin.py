from django.contrib import admin
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin

# Register your models here.
admin.site.register(Account)
admin.site.register(Lga)
admin.site.register(SenatorialZone)
admin.site.register(AdminUser)
admin.site.register(SuperUserAdmin)