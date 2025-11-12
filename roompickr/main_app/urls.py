from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('accounts/signup/', views.signup, name='signup'),
    path("rooms/", views.rooms_index, name="index"),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/<int:profile_id>/update/', views.update_profile, name='update_profile'),

    path("spaces/", views.SpaceList.as_view(), name="spaces_index"),
    path("spaces/<int:space_id>/detail", views.space_detail, name="spaces_detail"),
    path("spaces/create/", views.SpaceCreate.as_view(), name="spaces_create"),
    path("spaces/<int:pk>/update/", views.SpaceUpdate.as_view(), name="spaces_update"),
    path("spaces/<int:pk>/delete/", views.SpaceDelete.as_view(), name="spaces_delete"),

    path('spaces/<int:space_id>/add_feedback', views.add_feedback, name='add_feedback'),

]

