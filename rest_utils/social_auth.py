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


import json
import hmac
from base64 import b64encode
from hashlib import sha1
from requests import HTTPError
from social.exceptions import AuthCanceled, AuthTokenError
from social.backends.oauth import BaseOAuth1
from social.backends.linkedin import BaseLinkedinAuth


class LinkedinJSAPIOAuth(BaseLinkedinAuth, BaseOAuth1):
    """Linkedin OAuth authentication backend"""
    name = 'linkedin'
    SCOPE_SEPARATOR = '+'
    AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth/authenticate'
    REQUEST_TOKEN_URL = 'https://api.linkedin.com/uas/oauth/requestToken'
    ACCESS_TOKEN_URL = 'https://api.linkedin.com/uas/oauth/accessToken'
    ACCESS_TOKEN_METHOD = 'POST'

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        return self.get_json(
            self.user_details_url(),
            params={'format': 'json'},
            auth=self.oauth_auth(access_token),
            headers=self.user_data_headers()
        )

    def validate_bearer_token(self, token):
        """ Validate token provided by LinkedIN JSAPI. """
        data = ''.join([token[k] for k in token['signature_order']])
        secret = self.setting('SECRET')
        signature = b64encode(hmac.new(secret, data, sha1).digest())
        return signature == token['signature']

    def do_auth(self, access_token, *args, **kwargs):
        """ Exchange bearer token before finishing auth. """
        access_token = json.loads(access_token)

        if not self.validate_bearer_token(access_token):
            raise AuthTokenError(self)

        try:
            access_token = self.access_token(access_token)
        except HTTPError as err:
            if err.response.status_code == 400:
                raise AuthCanceled(self)
            else:
                raise

        return super(LinkedinJSAPIOAuth, self).do_auth(access_token)

    def access_token(self, token):
        """Return request for access token value"""
        data = {'xoauth_oauth2_access_token': token['access_token']}
        return self.get_querystring(self.ACCESS_TOKEN_URL, data=data,
                                    auth=self.oauth_auth(token),
                                    method=self.ACCESS_TOKEN_METHOD)
