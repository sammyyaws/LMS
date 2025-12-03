from django.contrib import admin
from .Models.user_models import userProfile
from .Models.course_models import Courses,Grade,Quiz,Assignment,Submission,Lessons,Course_categories,Progress
from .Models.roles_models import Role
# Register your models here.
admin.site.register(userProfile)
admin.site.register(Courses)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Lessons)
admin.site.register(Course_categories)
admin.site.register(Progress)
admin.site.register(Role)