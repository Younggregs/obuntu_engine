from django.contrib import admin
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, Ward, PollingUnit

# Register your models here.

class AccountSearch(admin.ModelAdmin):
    search_fields = ['name', 'phone', 'username']
  
admin.site.register(Account, AccountSearch)
admin.site.register(Lga)
admin.site.register(SenatorialZone)
admin.site.register(AdminUser)
admin.site.register(SuperUserAdmin)
admin.site.register(Ward)
admin.site.register(PollingUnit)