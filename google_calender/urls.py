from django.contrib import admin
from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView),
]
