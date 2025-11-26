from django.urls import path,include
from ..views import user_views

urlpatterns= [
path('register/',user_views.CreateUserAPI.as_view()),
path('update-user/<int:pk>/',user_views.UpdateUserAPI.as_view()),
path('login/',user_views.LoginUserView.as_view())
]