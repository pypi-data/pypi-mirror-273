try:
    import django_structlog
except ImportError:
    raise ImportError("ucam-observe[django] is required to use this module")


def hello_world_django():
    print("hello world Django")
    django_structlog
    return "hello world Django"
