from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.course_views import CourseViewSet, LessonViewSet  



router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('', include(router.urls)),
]
