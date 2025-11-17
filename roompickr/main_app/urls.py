from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/profile/<int:profile_id>/update/', views.update_profile, name='update_profile'),
    # reference: https://dev.to/davidomisakin/how-to-change-users-password-in-django-a-friendly-guide-556l
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
    path('change-password/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

    path("search/", views.SearchResultsView.as_view(), name="search_results"),

    path("spaces/your_spaces", views.your_spaces, name="your_spaces"),
    path("spaces/", views.space_all, name="space_all"),
    path("spaces/<int:space_id>/detail/", views.space_detail, name="detail"),
    path("spaces/create/", views.SpaceCreate.as_view(), name="spaces_create"),
    path("spaces/<int:pk>/update/", views.SpaceUpdate.as_view(), name="spaces_update"),
    path("spaces/<int:pk>/delete/", views.SpaceDelete.as_view(), name="spaces_delete"),

    path('spaces/<int:space_id>/add_feedback/<int:user_id>/', views.add_feedback, name='add_feedback'),
    path('spaces/<int:space_id>/edit_feedback/<int:feedback_id>/', views.edit_feedback, name='edit_feedback'),
    path('spaces/<int:space_id>/delete_feedback/<int:feedback_id>/', views.delete_feedback, name='delete_feedback'),

    path('spaces/<int:space_id>/add_image/', views.add_image, name='add_image'),
    path('spaces/<int:space_id>/update_image/<int:image_id>/', views.update_image, name='update_image'),
    path('spaces/<int:space_id>/delete_image/<int:image_id>/', views.delete_image, name='delete_image'),

    path('community/', views.questions, name='questions'),
    path('community/your_questions', views.your_questions, name='your_questions'),
    path('community/questions/<int:user_id>/', views.add_question, name='add_question'),
    path('community/question_detail/<int:question_id>/', views.question_detail, name='question_detail'),
    path('community/question_detail/<int:pk>/update_question/', views.QuestionUpdate.as_view(), name='update_question'),
    path('community/question_detail/<int:pk>/delete_question/', views.QuestionDelete.as_view(), name='delete_question'),
    path('community/answers/<int:user_id>/<int:question_id>/', views.add_answer, name='add_answer'),
    path('community/update_answers/<int:answer_id>/<int:question_id>/', views.update_answer, name='update_answer'),
    path('community/delete_answers/<int:answer_id>/<int:question_id>/', views.delete_answer, name='delete_answer'),

    path('spaces/<int:pk>/booking/', views.start_booking.as_view(), name='start_booking' ),
    path('space/<int:pk>/booking_detail/', views.BookingDetail.as_view(), name='booking_detail'),
    path("spaces/booking_history", views.booking_history, name="booking_history"),
]

