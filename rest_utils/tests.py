# -*- coding: utf-8 -*-
from mock import Mock

from django.http import Http404
from django_nose import FastFixtureTestCase as TestCase

from .permissions import DenyCreateOnPutPermission


class PermissionTest(TestCase):
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
