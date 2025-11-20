from django.contrib import admin
from .models.user_models import userProfile
from .models.course_models import courses
# Register your models here.
admin.site.register(userProfile)
admin.site.register(courses)