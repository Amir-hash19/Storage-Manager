from django.contrib import admin

from .models import File, Folder, ShareLink

admin.site.register(Folder)
admin.site.register(File)
admin.site.register(ShareLink)
