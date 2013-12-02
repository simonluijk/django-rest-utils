# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured

from rest_framework import views, status
from rest_framework import serializers
from rest_framework.response import Response

try:
    from social.apps.django_app.utils import load_strategy
    from social.apps.django_app.views import _do_login
    from social.exceptions import AuthAlreadyAssociated
except ImportError:
    raise ImproperlyConfigured("SocialAuthView require python-social-auth")


class SocialAuthSerializer(serializers.Serializer):
    """
    Serializer to receive social auth for python-social-auth
    """
    backend = serializers.CharField()
    access_token = serializers.CharField()


class SocialAuthView(views.APIView):
    """
    View to authenticate social auth tokens with python-social-auth. It accepts
    a token and backend. It will validate the token with the backend. If
    successful it returns the local user associated with the social user. If
    there is no associated user it will associate the current logged in user or
    create a new user if not logged in. The user is then logged in and returned
    to the client.
    """
    socal_seriliser = SocialAuthSerializer
    user_seriliser = None

    def post(self, request):
        serializer = self.socal_seriliser(data=request.DATA,
                                          files=request.FILES)

        if serializer.is_valid():
            backend = serializer.data['backend']
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request=request, backend=backend)
        try:
            kwargs = dict({(k, i) for k, i in serializer.data.items()
                          if k != 'backend'})
            user = request.user
            kwargs['user'] = user.is_authenticated() and user or None
            user = strategy.backend.do_auth(**kwargs)
        except AuthAlreadyAssociated:
            data = {
                'error_code': 'social_already_accociated',
                'status': 'Auth associated with another user.',
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        if not user:
            data = {
                'error_code': 'social_no_user',
                'status': 'No associated user.',
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            data = {
                'error_code': 'social_inactive',
                'status': 'Associated user is inactive.',
            }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        _do_login(strategy, user)

        if not self.user_seriliser:
            msg = 'SocialAuthView.user_seriliser should be a serializer.'
            raise ImproperlyConfigured(msg)
        serializer = self.user_seriliser(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
