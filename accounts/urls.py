from django.urls import path, include
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.UserSignUpView.as_view(), name='signup'),
]

