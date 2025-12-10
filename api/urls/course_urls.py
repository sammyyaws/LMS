from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.course_views import CourseViewSet, QuizViewSet   # adjust based on your structure

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')
router.register(r'quizzes', QuizViewSet, basename='quizzes')
urlpatterns = [
    path('', include(router.urls)),
]
