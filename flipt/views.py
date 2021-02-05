"""Django REST Framework views"""
from flipt_pb2 import ListFlagRequest
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from flipt.clients import client


class FeatureFlagListView(APIView):
    """View to retrieve all Flipt flags"""
    permission_classes = (AllowAny,)

    def get(self, _):
        response = client.ListFlags(ListFlagRequest())

        results = {}
        for flag in response.flags:
            results[flag.key] = flag.enabled

        return Response(results)
