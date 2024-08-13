from django.urls import include, path

urlpatterns = [
    path("protect/", include("protect.urls")),
]
