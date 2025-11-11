from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path("rooms/", views.rooms_index, name="index"),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/<int:profile_id>/update/', views.update_profile, name='update_profile'),
]

