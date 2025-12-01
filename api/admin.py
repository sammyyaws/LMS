from django.contrib import admin
from .Models.user_models import userProfile
from .Models.course_models import courses,grade,Quiz,Assignment,Submission,lessons,course_categories,progress
from .Models.roles_models import Role
# Register your models here.
admin.site.register(userProfile)
admin.site.register(courses)
admin.site.register(grade)
admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(lessons)
admin.site.register(course_categories)
admin.site.register(progress)
admin.site.register(Role)