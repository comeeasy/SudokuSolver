from django.urls import path
from . import views
from .views import CustomLoginView
from .views import logout_view

urlpatterns = [
    path('', views.front_page, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
path('logout/', logout_view, name='logout'),
]