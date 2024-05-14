# juntagrico-webdav

[![juntagrico-ci](https://github.com/juntagrico/juntagrico-webdav/actions/workflows/juntagrico-ci.yml/badge.svg?branch=main&event=push)](https://github.com/juntagrico/juntagrico-webdav/actions/workflows/juntagrico-ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/a597b9f0d54b836f1b46/maintainability)](https://codeclimate.com/github/juntagrico/juntagrico-webdav/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a597b9f0d54b836f1b46/test_coverage)](https://codeclimate.com/github/juntagrico/juntagrico-webdav/test_coverage)
[![image](https://img.shields.io/pypi/v/juntagrico-webdav.svg)](https://pypi.python.org/pypi/juntagrico-webdav)
[![image](https://img.shields.io/pypi/l/juntagrico-webdav.svg)](https://pypi.python.org/pypi/juntagrico-webdav)
[![image](https://img.shields.io/pypi/pyversions/juntagrico-webdav.svg)](https://pypi.python.org/pypi/juntagrico-webdav)
[![image](https://img.shields.io/pypi/status/juntagrico-webdav.svg)](https://pypi.python.org/pypi/juntagrico-webdav)
[![image](https://img.shields.io/pypi/dm/juntagrico-webdav.svg)](https://pypi.python.org/pypi/juntagrico-webdav/)
[![image](https://img.shields.io/github/last-commit/juntagrico/juntagrico-webdav.svg)](https://github.com/juntagrico/juntagrico-webdav)
[![image](https://img.shields.io/github/commit-activity/y/juntagrico/juntagrico-webdav)](https://github.com/juntagrico/juntagrico-webdav)
[![Requirements Status](https://requires.io/github/juntagrico/juntagrico-webdav/requirements.svg?branch=main)](https://requires.io/github/juntagrico/juntagrico-webdav/requirements/?branch=main)

This app allows to include webdav folders into juntagrico in order to share files with your members.

This is an extension for juntagrico. You can find more information about juntagrico here
(https://github.com/juntagrico/juntagrico).

# Installation

Install juntagrico-webdav via `pip`

    $ pip install juntagrico-webdav

or add it in your projects `requirements.txt`

In `settings.py` add `'juntagrico_webdav',` **before** juntagrico.

```python
INSTALLED_APPS = [
    ...
    'juntagrico_webdav',
    'juntagrico',
]
```

To avoid reloading the files list all the time, configure caching in `settings.py`

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'juntagrico_app_cache_table',
        'TIMEOUT': None,
    }
}
```

then run

    $ python -m manage createcachetable

In your `urls.py` you also need to extend the pattern:

```python
urlpatterns = [
    ...
    path('', include('juntagrico_webdav.urls')),
]
```
