from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.course_views import CourseViewSet, AssignmentViewSet,LessonViewSet   # adjust based on your structure




router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

router.register(r'assignments', AssignmentViewSet, basename='assignments')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls)),
]


