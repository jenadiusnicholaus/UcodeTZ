from django.contrib import admin
from .models import *


# Register your models here.

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('title',)
    search_fields = ['title', 'is_joined']
    prepopulated_fields = {'slug': ('title',)}


class TopicsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ("title",)
    search_fields = ['title', 'create']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Topics,TopicsAdmin)
admin.site.register(Courses, CourseAdmin)
admin.site.register( Category)
admin.site.register(Enrollment)
admin.site.register(EnrolledCourse)
admin.site.register(CourseOrder)
