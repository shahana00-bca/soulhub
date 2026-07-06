"""
URL configuration for soulhub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('home_get/',views.home_get),
    path('LandingPage/',views.LandingPage),

    path('logout/',views.logout),

    path('login_get/',views.login_get),
    path('login_post/',views.login_post),
    path('view_complaint_get/',views.view_complaint_get),
    path('view_feedback_get/',views.view_feedback_get),
    path('view_users_get/',views.view_users_get),
    path('view_review_get/',views.view_review_get),
    path('verify_psychologist_get/',views.verify_psychologist_get),
    path('view_psychologist_get/',views.view_psychologist_get),
    path('send_reply_get/<id>', views.send_reply_get),
    path('view_booking_get/', views.view_booking_get),
    path('view_payment_get/', views.view_payment_get),
    path('manage_schedule_get/', views.manage_schedule_get),
    path('chat_with_user_get/', views.chat_with_user_get),
    path('register_get/', views.register_get),
    path('change_password/', views.change_password),
    path('change_password_post/', views.change_password_post),

    path('psychologist_home/',views.psychologist_home),

    # path('psychologist_post/',views.psychologist_post),

    path('send_reply_post/', views.send_reply_post),
   # path('add_schedule_post/', views.add_schedule_post),
   # path('edit_schedule_post/', views.edit_schedule_post),
    path('edit_schedule_get/<id>', views.edit_schedule_get),
    path('edit_schedule_post/', views.edit_schedule_post),
    path('add_schedule_get/', views.add_schedule_get),
    path('add_schedule_post/', views.add_schedule_post),
    path('view_schedule_get/', views.view_schedule_get),
    path('view_schedule_post/', views.view_schedule_post),
    path('delete_schedule/<id>', views.delete_schedule),
    path('psy_bookings_get/<id>', views.psy_bookings_get),
    path('view_booking_get/', views.view_booking_get),
    path('approve_request/<id>', views.approve_request),
    path('reject_request/<id>', views.reject_request),
    path('user_register_post/',views.user_register_post),
    path('user_login_post/',views.user_login_post),
    path('view_psychologist_post/', views.view_psychologist_post),
    path('user_view_schedule_post/', views.user_view_schedule_post),
    path('user_send_feedback_post/', views.user_send_feedback_post),
    path('user_send_review_rating_post/', views.user_send_review_rating_post),
    path('send_complaint_viewreply_post/', views.send_complaint_viewreply_post),
    # path('chat_send/', views.chat_send),
    # path('chat_view/', views.chat_view),
    # path('chat2/', views.chat2),
    # path('chat1/', views.chat1),
    path('user_view_reply/', views.user_view_reply),
    # path('dairy_post', views.dairy_post),
    # path('view_reply_post', views.view_reply_post),

    path('psychologist_post/',views.psychologist_post),

    path('user_book_appointment_post/',views.user_book_appointment_post),

    path('user_chat/',views.user_chat),
    path('send_byst/',views.send_byst),
    path('user_add_diary/',views.user_add_diary),
    path('user_view_diary/',views.user_view_diary),
    path('recommend_psychologist/',views.recommend_psychologist),
    path('view_appointment_get/',views.view_appointment_get),
    path('approve_appointment/<id>',views.approve_appointment),
    path('reject_appointment/<id>',views.reject_appointment),
    path('view_approved_appointment/',views.view_approved_appointment),


    path('psychologist_view_user/',views.psychologist_view_user),
    path('psychologist_chat_to_user/<id>',views.psychologist_chat_to_user),
    path('psy_chat_view_user/',views.psy_chat_view_user),
    path('psy_chat_send_user/<str:msg>',views.psy_chat_send_user),


    path('view_appointment_get/',views.view_appointment_get),

    path('payment_success/',views.payment_success),

    path('accept_psychologist/<id>',views.accept_psychologist),
    path('reject_psychologist/<id>',views.reject_psychologist),
    path('approved_psy/',views.approved_psy),

    path('psy_chat_to_user/<int:id>',views.psy_chat_to_user),
    path('psy_chat_send_user_new/<str:msg>',views.psy_chat_send_user_new),
    path('chat_view/',views.chat_view),

    path('user_viewchat/',views.user_viewchat),
    path('user_sendchat/',views.user_sendchat),


    path('user_view_psychologyst_googlemeet_link/',views.user_view_psychologyst_googlemeet_link),

    path('psy_add_google_meet_link/',views.psy_add_google_meet_link),
    path('psy_view_link/',views.psy_view_link),
    path('psy_delete_link/<id>',views.psy_delete_link),

    path('user_send_schedule_rating/', views.user_send_schedule_rating),

]
