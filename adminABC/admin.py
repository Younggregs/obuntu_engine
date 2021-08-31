from django.contrib import admin
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, Ward, PollingUnit, DemoAccount, Post, Comment

# Register your models here.

class AccountSearch(admin.ModelAdmin):
    search_fields = ['firstname', 'phone', 'firstname', 'middlename', "lastname"]


class PollSearch(admin.ModelAdmin):
    search_fields = ['name', 'delimitation']


class WardSearch(admin.ModelAdmin):
    search_fields = ['id', 'name']
  
admin.site.register(Account, AccountSearch)
admin.site.register(Lga)
admin.site.register(SenatorialZone)
admin.site.register(AdminUser)
admin.site.register(SuperUserAdmin)
admin.site.register(Ward, WardSearch)
admin.site.register(PollingUnit, PollSearch)

#Demo
class DemoAccountSearch(admin.ModelAdmin):
    search_fields = ['firstname', 'phone', 'firstname', 'middlename', "lastname"]

admin.site.register(DemoAccount, DemoAccountSearch)
admin.site.register(Post)
admin.site.register(Comment)