from django.urls import path
from . import views

urlpatterns = [
    path(r'^calendar/', views.CalendarView.as_view(), name='calendar'),
    path('mail_sent/', views.mail_sent, name='mail_sent'),
    path(r'^email-users/$',
         views.SendUserEmails.as_view(),
         name='email'),
]