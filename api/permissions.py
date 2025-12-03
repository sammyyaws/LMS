from rest_framework.permissions import BasePermission
from .Models.user_models import userProfile

####permission class for superadmin
class isSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
           hasattr(request.user, "userProfile") and
           request.user.userProfile.role.role_name=='superadmin'
        )

###permission class for admin
class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
           hasattr(request.user, "userProfile") and
           request.user.userProfile.role.role_name=='admin'
        )


        ###permission class for instructor
class isInstructor(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
           hasattr(request.user, "userProfile") and
           request.user.userProfile.role.role_name=='instructor'
        )

        ###permission class for admin
class is_student(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
           hasattr(request.user, "userProfile") and
           request.user.userProfile.role.role_name=='student'
        )

###permission class for admin and instructor
class is_Admin_or_Instructor (BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
           hasattr(request.user, "userProfile") and
           request.user.userProfile.role.role_name in ['admin', 'instructor']
        )