"""Testing Flipt-related information"""


def test_version():
    try:
        from flipt import __version__
    except ImportError:
        __version__ = None

    assert __version__ is not None
