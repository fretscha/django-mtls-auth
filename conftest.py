import pytest

good_headers = {
    "Content-Type": "application/json",
    "X-Ssl-User-Dn": "O=MyOrg,L=Bern,ST=Bern,C=CH,GN=test,SN=client,E=test.client@client.tld,CN=Test Client (user2845)",
    "X-Ssl-Issuer-Dn": "O=MyOrg,L=Bern,ST=Bern,C=CH,CN=DummyCA Root CA",
    "X-Ssl-Authenticated": "SUCCESS",
}

bad_headers = {
    "Content-Type": "application/json",
    "X-Ssl-User-Dn": "O=MyOrg,L=Bern,ST=Bern,C=CH,GN=test,SN=client,E=test.client@client.tld,CN=Test Client (user2845)",
    "X-Ssl-Issuer-Dn": "O=MyOrg,L=Bern,ST=Bern,C=CH,CN=DummyCA Root CA",
    "X-Ssl-Authenticated": "FAILURE",
}


@pytest.fixture
def success_client():
    from django.test import Client

    return Client(headers=good_headers)


@pytest.fixture
def fail_client():
    from django.test import Client

    return Client(headers=bad_headers)
