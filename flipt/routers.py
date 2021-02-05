"""Flipt router for Django REST Framework"""
from rest_framework.routers import DefaultRouter

from flipt.decorators import flag_check


class FlaggedRouter(DefaultRouter):
    """
    Usage:

    router = FlaggedRouter()
    router.register('test', TestViewSet, flag_key='flag_key', flag_state=True)

    * `flag_state` is not required
    """
    flagged_infos = {}

    def register(self, prefix, viewset, basename=None, flag_key: str = None,
                 flag_state=True):
        super().register(prefix, viewset, basename=basename)

        if flag_key:
            self.flagged_infos[viewset] = {
                'flag_key': flag_key,
                'state': flag_state
            }

    def get_urls(self):
        urls = super().get_urls()
        for url in urls:
            flagged_info = self.flagged_infos.get(url.callback.cls)
            if not flagged_info:
                continue

            flagged_view = flag_check(**flagged_info)(url.callback)
            url.callback = flagged_view

        return urls
