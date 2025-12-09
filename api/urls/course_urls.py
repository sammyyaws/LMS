from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.course_views import CourseViewSet   # adjust based on your structure

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('', include(router.urls)),
]
