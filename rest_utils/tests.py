# -*- coding: utf-8 -*-
from mock import Mock

from django.http import Http404
from django.contrib.auth import get_user_model
from django_nose import FastFixtureTestCase as TestCase

from rest_framework import serializers

from .permissions import DenyCreateOnPutPermission, NotAuthenticatedPermission
from .user import UniqueEmailUserSerializerMixin, PasswordSerializerMixin


class PermissionsTest(TestCase):
    def test_deny_create_on_put_permission(self):
        permission = DenyCreateOnPutPermission()
        view = Mock()
        request = Mock()

        request.method = 'GET'
        self.assertTrue(permission.has_permission(request, view))

        request.method = 'PUT'
        self.assertTrue(permission.has_permission(request, view))

        request.method = 'PUT'
        view.get_object = Mock(side_effect=Http404)
        self.assertFalse(permission.has_permission(request, view))

    def test_not_authenticated_permission(self):
        permission = NotAuthenticatedPermission()

        view = Mock()
        request = Mock()

        request.user.is_authenticated = Mock(return_value=True)
        self.assertFalse(permission.has_permission(request, view))

        request.user.is_authenticated = Mock(return_value=False)
        self.assertTrue(permission.has_permission(request, view))


class UserSerializer(UniqueEmailUserSerializerMixin, PasswordSerializerMixin,
                     serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'password')


class UserSerializerTest(TestCase):
    def test_validate_email(self):
        """
        Test the same email can not be used twice.
        """
        data = {
            'email': 'user1@example.com',
            'password': 'testpassword',
        }
        get_user_model().objects.create(email='user1@example.com')
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(serializer.error_messages['email_exists'],
                      serializer.errors['email'])

        user = Mock()
        user.email = 'user1@example.com'
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid())
        with self.assertRaises(KeyError):
            serializer.errors['email']

    def test_password_is_set(self):
        data = {
            'email': 'user2@example.com',
            'password': 'testpassword',
        }

        user = Mock()
        user.email = 'user1@example.com'
        serializer = UserSerializer(user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        user.set_password.assert_called_once_with('testpassword')
        self.assertNotIn('password', serializer.data.keys())
