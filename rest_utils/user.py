# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UniqueEmailUserSerializerMixin(object):
    """
    Mixin that verifies the email is not in use.
    """
    default_error_messages = {
        'email_exists': 'Email already in use!'
    }

    def validate_email(self, attrs, source):
        try:
            email = attrs[source]
        except KeyError:
            return attrs

        users_qs = get_user_model().objects.filter(email=email)
        if self.object:
            users_qs = users_qs.exclude(email=self.object.email)

        if users_qs.count() > 0:
            msg = self.error_messages['email_exists']
            raise serializers.ValidationError(msg)

        return attrs
