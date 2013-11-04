# -*- coding: utf-8 -*-
from django.exceptions import ImproperlyConfigured

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
    token = serializers.CharField()
    code = serializers.CharField()


class SocialAuthView(views.APIView):
    """
    View to authenticate social auth tokens with python-social-auth. It accepts
    a token and backend. It will validate the token with the backend. If
    successfully it returns the local user associated with the social user. If
    there is no associated user it will associate the current logged in user or
    create a new user in not logged in. The user is then logged in and returned
    to the client.
    """
    user_seriliser = None

    def post(self, request):
        serializer = SocialAuthSerializer(data=request.DATA,
                                          files=request.FILES)

        if serializer.is_valid():
            backend = serializer.data['backend']
            auth_token = serializer.data['token']
            code = serializer.data['code']
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request=request, backend=backend)
        try:
            user = strategy.backend.do_auth(
                access_token=auth_token, code=code,
                user=request.user.is_authenticated() and request.user or None
            )
        except AuthAlreadyAssociated:
            return Response({'status': 'Auth associated with another user.'},
                            status=status.HTTP_403_FORBIDDEN)

        if not user.is_active:
            return Response({'status': 'Associated user is inactive.'},
                            status=status.HTTP_403_FORBIDDEN)

        _do_login(strategy, user)

        if not self.user_seriliser:
            msg = 'SocialAuthView.user_seriliser should be a serializer.'
            raise ImproperlyConfigured(msg)
        serializer = self.user_seriliser(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
