# -*- coding: utf-8 -*-
from django.http import Http404
from rest_framework import permissions


class DenyCreateOnPutPermission(permissions.BasePermission):
    """
    Prevent creating object on PUT
    """
    def has_permission(self, request, view):
        if request.method == 'PUT':
            try:
                view.get_object()
            except Http404:
                return False
        return True


class NotAuthenticatedPermission(permissions.BasePermission):
    """
    Deny access to authenticated users.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return False
        return True
