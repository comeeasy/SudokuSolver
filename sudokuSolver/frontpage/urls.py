from django.urls import path
from . import views

urlpatterns = [
    path('', views.front_page, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
]