from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone
from ..Models.course_models import Courses, Assignment,Progress
from ..serializers.course_serializers import CourseSerializer, AssignmentSerializer, ProgressSerializer
from ..permissions import isAdmin, isSuperAdmin, isSuperAdmin_Admin_Instructor, is_student

class CourseViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Courses
    """
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer

    # Only admins or instructors or superadmin can create/update courses
    permission_classes = [permissions.IsAuthenticated ,isSuperAdmin_Admin_Instructor]


    def perform_create(self, serializer):
        """Automatically set creator to logged-in user"""
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        """Protect sensitive fields"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Remove fields from request data that shouldn't be updated
        data = request.data.copy()
        data.pop('creator_id', None)
        data.pop('approved_by', None)
        data.pop('status', None)  # Only admins/superadmins can change status

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[isAdmin | isSuperAdmin]
    )
    def approve(self, request, pk=None):
        """
        Custom endpoint to approve a course.
        Only admin or superadmin can call this.
        """
        course = self.get_object()
        course.status = "approved"
        course.approved_by = request.user
        course.approved_at = timezone.now()
        course.save()
        serializer = self.get_serializer(course)
        return Response(serializer.data)
    






class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.select_related("course", "lesson").all()
    serializer_class = AssignmentSerializer

    # --------------------------
    # PERMISSION HANDLING
    # --------------------------
    def get_permissions(self):
        """
        - Anyone authenticated can READ (list/retrieve)
        - Only SuperAdmin, Admin or Instructor can CREATE, UPDATE, DELETE
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]   # Students also have access
        else:
            permission_classes = [isSuperAdmin_Admin_Instructor]

        return [permission() for permission in permission_classes]

    # --------------------------
    # CREATE OVERRIDE
    # --------------------------
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        assignment = serializer.save()

        return Response(
            AssignmentSerializer(assignment).data,
            status=status.HTTP_201_CREATED
        )

    # --------------------------
    # UPDATE OVERRIDE
    # --------------------------
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_assignment = serializer.save()

        return Response(AssignmentSerializer(updated_assignment).data)

    # --------------------------
    # PARTIAL UPDATE (PATCH)
    # --------------------------
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_assignment = serializer.save()

        return Response(AssignmentSerializer(updated_assignment).data)

    # --------------------------
    # DELETE OVERRIDE
    # --------------------------
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"message": "Assignment deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )



class ProgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all().select_related("user", "course", "lesson")
    serializer_class = ProgressSerializer

    # -----------------------------
    # PERMISSIONS
    # -----------------------------
    def get_permissions(self):

        # Students can only view their own progress
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]

        # Only SuperAdmin, Admin, or Instructor can CREATE, UPDATE, or DELETE
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [isSuperAdmin_Admin_Instructor()]

        return [permissions.IsAuthenticated()]

    # -----------------------------
    # LIMIT STUDENT VISIBILITY
    # -----------------------------
    def get_queryset(self):
        user = self.request.user

        # If student → only return their own progress records
        if hasattr(user, "userProfile") and user.userProfile.role.role_name == "student":
            return Progress.objects.filter(user=user)

        # For admin roles → return everything
        return Progress.objects.all()

    # -----------------------------
    # ENSURE STUDENT CANNOT CREATE
    # -----------------------------
    def create(self, request, *args, **kwargs):
        user = request.user

        # Block students from creating progress
        if hasattr(user, "userProfile") and user.userProfile.role.role_name == "student":
            return Response(
                {"detail": "Students cannot create progress records manually."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().create(request, *args, **kwargs)