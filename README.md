
# django-tls-auth

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/{owner}/{repo}/CI?label=build)
![Beta](https://img.shields.io/badge/beta-8A2BE2)

Enable mTLS authetication to your Django project

Documentation
-------------

The full documentation is at https://django-tls-auth.readthedocs.io.

Quickstart
----------

Install django-tls-auth
```shell script
    pip install django-tls-auth
```

Add it to your `MIDDLEWARE`

```python python
    MIDDLEWARE = [
    ...
    "tls_auth.middleware.TLSAuthenticationMiddleware",
    ]
```


# Features

* TODO

# Running Tests

Does the code actually work?
```shell script
    cd django-tls-auth
    poetry install
    poetry run pytests.py
````

# Credits

Tools used in rendering this package:

* [cookiecutter](https://github.com/audreyr/cookiecutter)
* [django-reusable-app](https://github.com/AndreGuerra123/django-reusable-app)
