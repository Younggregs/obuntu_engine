from django.contrib import admin
from .models import Account, Lga, SenatorialZone, AdminUser, SuperUserAdmin, Ward, PollingUnit, Post, Comment, Like, Video, VideoCategory, Chat

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
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Video)
admin.site.register(VideoCategory)
admin.site.register(Chat)