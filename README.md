# Django-rest-utils

**Utils to help building a REST API with django-rest-framework.**

[![build-status]][travis]

# Overview

OVERVIEW

# Requirements

* Python (2.6, 2.7, 3.3)
* Django (1.5, 1.6)
* python-social-auth if using SocialAuthView

# Installation

Install using `pip`...

    pip install django-rest-utils


# Example

EXAMPLE

That's it, we're done!

[build-status]: https://secure.travis-ci.org/simonluijk/django-rest-utils.png?branch=master
[travis]: http://travis-ci.org/simonluijk/django-rest-utils?branch=master


# Change log

## Version 0.0.4

* Americanize spellings. Two attributes of `SocialAuthView` have changed.
`socal_seriliser` became `socal_seriliser` and `user_seriliser` became
`user_serializer`. These are minor backward incompatible changes.

## Version 0.0.3

* Added LinkedinJSAPIOAuth

## Version 0.0.2

* Removed user serializer mixins.
* Added CreateModelMixin.
* Allow SocialAuthSerializer to swapped in SocialAuthView.

## Version 0.0.1

* Initial version.
