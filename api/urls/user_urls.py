from django.urls import path,include
from ..views import user_views

urlpatterns= [
path('register/',user_views.CreateUserAPI.as_view()),
path('update-user',user_views.UpdateUserAPI.as_view())
]