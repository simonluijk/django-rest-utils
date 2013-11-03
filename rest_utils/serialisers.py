# -*- coding: utf-8 -*-
from rest_framework import serializers


class SocialAuthSerializer(serializers.Serializer):
    """
    Serializer to receive social auth for Python-social-auth
    """
    backend = serializers.CharField()
    token = serializers.CharField()
    code = serializers.CharField()
