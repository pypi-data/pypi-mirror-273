from django.urls import path
from .views import ping
from .views import echo
from .views import getRequestInfo

urlpatterns = [
    path("ping", ping),
    path("echo", echo),
    path("getRequestInfo", getRequestInfo),
]
