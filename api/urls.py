from django.urls import path,include
from . import views

urlpatterns= [
path('register/',views.CreateUserAPI.as_view()),
path('update-user',views.UpdateUserAPI.as_view())
]