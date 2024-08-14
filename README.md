
# django-mtls-auth

![Beta](https://img.shields.io/badge/beta-red)
![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Ffretscha%2Fdjango-mtls-auth%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&label=latest%20release)



This Django middleware package enables authentication via request headers sent by an ingress reverse proxy. It provides a seamless way to integrate with existing reverse proxy setups, allowing developers to authenticate users based on headers such as `X-SSL-User-DN`. This approach is particularly useful in microservices architectures, where the reverse proxy handles authentication upstream. This package is designed to be easily configurable, supporting various header names and formats, ensuring flexibility and adaptability to different environments. With this middleware, developers can enhance security and streamline user management across distributed systems, making it an ideal choice for projects leveraging reverse proxies for authentication.


Documentation
-------------

~~The full documentation is at https://django-mtls-auth.readthedocs.io.~~

Quickstart
----------

Install django-mtls-auth
```shell script
pip install django-mtls-auth
```

Add it to your `MIDDLEWARE`

```python
MIDDLEWARE = [
    ...
    "mtls_auth.middleware.MTLSAuthenticationMiddleware",
]
```

# Features

- [x] Authentication 
- [ ] Documentation 
- [ ] Authorization 
- [ ] Audit 


# Running Tests

Does the code actually work?
```shell script
cd django-mtls-auth
poetry install

poetry run pytest
# or 
poetry run nox
````


# Credits

Tools used in rendering this package:

* [cookiecutter](https://github.com/audreyr/cookiecutter)
* [django-reusable-app](https://github.com/AndreGuerra123/django-reusable-app)
