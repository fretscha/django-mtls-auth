from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import path


# return all request headers as json
def get_headers(request):
    return JsonResponse(dict(request.headers))


@login_required
def protected(request):
    return JsonResponse({"message": f"You ({request.user}) are logged in!"})


def login(request):
    return JsonResponse({"message": "You need to login"})


urlpatterns = [
    path("headers/", get_headers, name="get_headers"),
    path("protected/", protected, name="protected"),
    path("login/", login, name="login"),
]
