"""Flipt flag-related functions"""
from django.conf import settings
from flipt_pb2 import EvaluationRequest
from grpc import RpcError

from flipt.clients import client


def flag_enabled(flag_key: str, user=None) -> bool:
    if hasattr(settings, 'FLIPT_FLAG_OVERRIDDEN'):
        override_value = settings.FLIPT_FLAG_OVERRIDDEN.get(flag_key)
        if override_value is not None:
            return bool(override_value)

    if client is None:
        return getattr(settings, 'FLIPT_FLAG_DEFAULT', True)

    request = EvaluationRequest(
        flag_key=flag_key,
        entity_id=user.username if user and user.username else '_'
    )

    try:
        client.Evaluate(request)
    except RpcError:
        # TODO: catch error
        return False

    return True


def flag_disabled(flag_key: str, user=None) -> bool:
    return not flag_enabled(flag_key, user)
