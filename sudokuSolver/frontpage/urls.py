from django.urls import path
from . import views
from .views import login_view
from .views import logout_view
from .views import send_verification_email

urlpatterns = [
    path('', views.front_page, name='home'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('send_verification_email/', send_verification_email, name='send_verification_email'),
]