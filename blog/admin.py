from django.contrib import admin
from .models import *


class postAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ['title', 'publish']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post,postAdmin)
