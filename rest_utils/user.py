# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UniqueEmailUserSerializerMixin(object):
    """
    Mixin that verifies the email is not in use.
    """
    default_error_messages = {
        'email_exists': 'User with this Email address already exists.'
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


class PasswordSerializerMixin(object):
    """
    Mixin that sets the user password and strips it from the output.
    """
    def to_native(self, *args, **kwargs):
        try:
            self.fields.pop('password')
        except KeyError:
            pass
        return super(PasswordSerializerMixin, self).to_native(*args, **kwargs)

    def restore_object(self, attrs, instance=None):
        self.passwd = attrs.pop('password')
        self.fields.pop('password')

        return super(PasswordSerializerMixin, self).restore_object(attrs,
                                                                   instance)

    def save_object(self, obj, **kwargs):
        if self.passwd:
            obj.set_password(self.passwd)
        super(PasswordSerializerMixin, self).save_object(obj, **kwargs)
