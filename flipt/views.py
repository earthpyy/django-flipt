"""Django REST Framework views"""
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from flipt_pb2 import ListFlagRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from flipt.clients import client


try:
    CACHE_SECONDS = settings.CACHE_SECONDS
except AttributeError:
    CACHE_SECONDS = 0


class FeatureFlagListView(APIView):
    """View to retrieve all Flipt flags"""
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(CACHE_SECONDS))
    def get(self, _):
        if client is None:
            default = getattr(settings, 'FLAG_DEFAULT', True)
            return Response({'_default': default})

        response = client.ListFlags(ListFlagRequest())

        results = {}
        for flag in response.flags:
            results[flag.key] = flag.enabled

        return Response(results)
