from django.contrib import admin
from .models import *


class PinsAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author', 'collection', 'video', 'image')
    list_display_links = ('author', 'collection')


admin.site.register(Pins)
admin.site.register(Likes)
admin.site.register(Collections)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Report)
admin.site.register(Follow)
admin.site.register(Notification)
