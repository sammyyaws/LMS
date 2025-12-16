from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from ..Models.course_models import Courses, Quizzes
from ..serializers.course_serializers import CourseSerializer, QuizSerializer
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
    


###Quiz Viewset 1
class QuizViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Quizzes
    """
    queryset = Quizzes.objects.all()
    serializer_class = CourseSerializer  # Adjust to QuizSerializer when available

    # Only admins or instructors or superadmin can create/update quizzes
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
    

###Quiz Viewset 2
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quizzes.objects.all().order_by("-date_created")
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]  # optional

    def create(self, request, *args, **kwargs):
        """Override create to give a cleaner response."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                "message": "Quiz created successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Override update for cleaner output."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                "message": "Quiz updated successfully",
                "data": serializer.data
            }
        )
