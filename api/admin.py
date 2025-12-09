from django.contrib import admin
from .Models.user_models import userProfile
from .Models.course_models import Courses,Grade,Quiz,Assignment,Submission,Lessons,Course_categories,Progress
from .Models.roles_models import Role
from django.utils import timezone

##creating a custom action to approve pending courses
@admin.action(description="Approve selected courses")
def approve_courses(modeladmin, request, queryset):
    # Check if the user has userProfile and the right role
    if hasattr(request.user, "userProfile") and request.user.userProfile.role.role_name in ["admin", "superadmin"]:
        queryset.update(
            status="approved",
            approved_by=request.user,
            approved_at=timezone.now()
        )
    else:
        # Optionally, raise a warning if they are not allowed
        from django.contrib import messages
        messages.error(request, "You do not have permission to approve courses.")

class CoursesAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "creator", "approved_by", "approved_at")
    list_filter = ("status", "category")
    actions = [approve_courses] # Register the custom action










# Register your models here.
admin.site.register(userProfile)
admin.site.register(Courses, CoursesAdmin)
admin.site.register(Grade)
admin.site.register(Quiz)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Lessons)
admin.site.register(Course_categories)
admin.site.register(Progress)
admin.site.register(Role)