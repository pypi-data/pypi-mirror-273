# juntagrico-pg


[![juntagrico-ci](https://github.com/juntagrico/juntagrico-pg/actions/workflows/juntagrico-ci.yml/badge.svg?branch=main&event=push)](https://github.com/juntagrico/juntagrico-pg/actions/workflows/juntagrico-ci.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/02bb5f131cc157fcc4b9/maintainability)](https://codeclimate.com/github/juntagrico/juntagrico-pg/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/02bb5f131cc157fcc4b9/test_coverage)](https://codeclimate.com/github/juntagrico/juntagrico-pg/test_coverage)
[![image](https://img.shields.io/pypi/v/juntagrico-pg.svg)](https://pypi.python.org/pypi/juntagrico-pg)
[![image](https://img.shields.io/pypi/l/juntagrico-pg.svg)](https://pypi.python.org/pypi/juntagrico-pg)
[![image](https://img.shields.io/pypi/pyversions/juntagrico-pg.svg)](https://pypi.python.org/pypi/juntagrico-pg)
[![image](https://img.shields.io/pypi/status/juntagrico-pg.svg)](https://pypi.python.org/pypi/juntagrico-pg)
[![image](https://img.shields.io/pypi/dm/juntagrico-pg.svg)](https://pypi.python.org/pypi/juntagrico-pg/)
[![image](https://img.shields.io/github/last-commit/juntagrico/juntagrico-pg.svg)](https://github.com/juntagrico/juntagrico-pg)
[![image](https://img.shields.io/github/commit-activity/y/juntagrico/juntagrico-pg)](https://github.com/juntagrico/juntagrico-pg)

postgres db editor for juntagrico.

This is an extension for juntagrico. You can find more information about juntagrico here
(https://github.com/juntagrico/juntagrico)

# Installation

Install juntagrico-pg via `pip`

    $ pip install juntagrico-pg

or add it in your projects `requirements.txt`

In `settings.py` add `'juntagrico_pg',` **before** juntagrico.

```python
INSTALLED_APPS = [
    ...
    'juntagrico_pg',
    'juntagrico',
]
```

In your `urls.py` you also need to extend the pattern:

```python
urlpatterns = [
    ...
    path('', include('juntagrico_pg.urls')),
]
```
