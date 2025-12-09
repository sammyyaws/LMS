from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone
from ..Models.course_models import Courses, Assignment
from ..serializers.course_serializers import CourseSerializer, AssignmentSerializer
from ..permissions import isAdmin, isSuperAdmin, isSuperAdmin_Admin_Instructor, is_student
from ..Models.course_models import Courses,Lessons
from ..serializers.course_serializers import CourseSerializer,LessonSerializer
from ..permissions import isAdmin, isSuperAdmin, isSuperAdmin_Admin_Instructor

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





###################### views  for the lessons ########################


class LessonViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Lessons
    """
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, isSuperAdmin_Admin_Instructor]

    def perform_create(self, serializer):
        """
        Automatically associate lesson with the given course.
        The frontend must send 'course_id' in the request data.
        """
        course_id = self.request.data.get("course_id")
        if not course_id:
            raise serializers.ValidationError({"course_id": "This field is required."})

        try:
            course = Courses.objects.get(id=course_id)
        except Courses.DoesNotExist:
            raise serializers.ValidationError({"course_id": "Course not found."})

        serializer.save(course=course)

    def update(self, request, *args, **kwargs):
        """
        Protect sensitive fields on update.
        """
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()

        # Prevent changing the course once created (optional)
        data.pop("course_id", None)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)