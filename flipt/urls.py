from functools import partial

from django.urls import URLPattern
from django.urls.resolvers import RoutePattern, RegexPattern, URLResolver
from flipt.flags import flag_enabled


class FlaggedURLResolver(URLResolver):
    def __init__(self, *args, flag_key: str = None, flag_state=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag_key = flag_key
        self.flag_state = flag_state

    def resolve(self, path):
        if self.flag_key is None:
            return super().resolve(path)

        matched = flag_enabled(self.flag_key) == self.flag_state
        if matched:
            return super().resolve(path)


class FlaggedURLPattern(URLPattern):
    def __init__(self, *args, flag_key: str = None, flag_state=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.flag_key = flag_key
        self.flag_state = flag_state

    def resolve(self, path):
        if self.flag_key is None:
            return super().resolve(path)

        matched = flag_enabled(self.flag_key) == self.flag_state
        if matched:
            return super().resolve(path)


def _flagged_path(route, view, kwargs=None, name=None, flag_key: str = None, flag_state=True, Pattern=None):
    if isinstance(view, (list, tuple)):
        # For include(...) processing.
        pattern = Pattern(route, is_endpoint=False)
        urlconf_module, app_name, namespace = view
        return FlaggedURLResolver(
            pattern,
            urlconf_module,
            kwargs,
            app_name=app_name,
            namespace=namespace,
            flag_key=flag_key,
            flag_state=flag_state,
        )
    elif callable(view):
        pattern = Pattern(route, name=name, is_endpoint=True)
        return FlaggedURLPattern(
            pattern,
            view,
            kwargs,
            name,
            flag_key=flag_key,
            flag_state=flag_state,
        )
    else:
        raise TypeError('view must be a callable or a list/tuple in the case of include().')


flagged_path = partial(_flagged_path, Pattern=RoutePattern)
flagged_re_path = partial(_flagged_path, Pattern=RegexPattern)
