from django.contrib import admin
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, Ward, PollingUnit, Post, Comment, Like

# Register your models here.
admin.site.register(Account)
admin.site.register(Lga)
admin.site.register(SenatorialZone)
admin.site.register(AdminUser)
admin.site.register(SuperUserAdmin)
admin.site.register(Ward)
admin.site.register(PollingUnit)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)