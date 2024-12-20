"""
URL configuration for tg_auth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app.views import login_with_telegram_view, check_status_view, telegram_webhook

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_with_telegram_view, name='login_page'),
    path('check_status/', check_status_view, name='check_status'),
    path('telegram-webhook/', telegram_webhook, name='telegram_webhook'),
]
