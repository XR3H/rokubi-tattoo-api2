from django.urls import path
from telegram_api.views import NotifyAPI

urlpatterns = [
    path('notify/', NotifyAPI.as_view()),
]