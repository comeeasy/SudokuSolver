from django.urls import path
from . import views

urlpatterns = [
    path('bytype/', views.solveByType),
    path('bypic/', views.solveByPic),
    path('posts/', views.posts)
]