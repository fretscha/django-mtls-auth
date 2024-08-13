from django.urls import path

from . import views

app_name = "protect"

urlpatterns = [
    path("headers/", views.get_headers, name="get_headers"),
    path("protected/", views.protected, name="protected"),
    path("login/", views.login, name="login"),
]
