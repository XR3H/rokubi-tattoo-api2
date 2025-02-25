from django.urls import path, include

urlpatterns = [
    path('telegram/', include('telegram_api.urls'))
]
