"""Flipt decorators"""
from functools import wraps
from typing import Dict

from django.http import Http404
from django.test import override_settings

from flipt.flags import flag_enabled


# pylint: disable=invalid-name
class override_flags(override_settings):
    def __init__(self, flags: Dict[str, bool]):
        flags_setting = {}

        for flag_key, value in flags.items():
            if isinstance(value, bool):
                flags_setting[flag_key] = value

        super().__init__(FLAG_OVERRIDDEN=flags_setting)


def flag_check(flag_key: str, state=True):
    def decorator(func):
        def inner(request, *args, **kwargs):
            enabled = flag_enabled(flag_key, user=request.user)

            if bool(state) == bool(enabled):
                return func(request, *args, **kwargs)
            raise Http404

        return wraps(func)(inner)

    return decorator
