from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
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