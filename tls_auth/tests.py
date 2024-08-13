import uuid

import pytest
from django.urls import reverse

from .settings import ISSUER_DN_HEADER, SUCCESS_HEADER, USER_DN_HEADER


@pytest.fixture
def test_password():
    return "strong-test-pass"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.mark.django_db
def test_user_create(django_user_model, create_user):
    create_user(username="testuser1")
    create_user(username="testuser2")
    assert django_user_model.objects.count() == 2


@pytest.mark.django_db
def test_get_good_headers_view(success_client):
    response = success_client.get(reverse("get_headers"))
    assert response.status_code == 200
    headers = {k.upper(): v for k, v in response.wsgi_request.headers.items()}
    assert headers.get(SUCCESS_HEADER) == "SUCCESS"
    assert (
        headers.get(USER_DN_HEADER)
        == "O=MyOrg,L=Bern,ST=Bern,C=CH,GN=test,SN=client,E=test.client@client.tld,CN=Test Client (user2845)"
    )
    assert headers.get(ISSUER_DN_HEADER) == "O=MyOrg,L=Bern,ST=Bern,C=CH,CN=DummyCA Root CA"


@pytest.mark.django_db
def test_get_bad_headers_view(fail_client):
    response = fail_client.get(reverse("get_headers"))
    assert response.status_code == 200
    headers = {k.upper(): v for k, v in response.wsgi_request.headers.items()}
    assert headers.get(SUCCESS_HEADER) == "FAILURE"
    assert (
        headers.get(USER_DN_HEADER)
        == "O=MyOrg,L=Bern,ST=Bern,C=CH,GN=test,SN=client,E=test.client@client.tld,CN=Test Client (user2845)"
    )


@pytest.mark.django_db
def test_get_protected_view(success_client):
    response = success_client.get(reverse("protected"))
    assert response.status_code == 200
    assert response.json() == {"message": "You (Test Client (user2845)) are logged in!"}


@pytest.mark.django_db
def test_fail_protected_view(fail_client):
    response = fail_client.get(reverse("protected"))
    assert response.status_code == 302
    assert response.url == "/login/?next=/protected/"
