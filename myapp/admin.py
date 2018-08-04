from django.contrib import admin
from .models import File, Directory

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    pass