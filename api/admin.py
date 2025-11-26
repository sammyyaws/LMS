from django.contrib import admin
from .Models.user_models import userProfile
from .Models.course_models import courses
# Register your models here.
admin.site.register(userProfile)
admin.site.register(courses)