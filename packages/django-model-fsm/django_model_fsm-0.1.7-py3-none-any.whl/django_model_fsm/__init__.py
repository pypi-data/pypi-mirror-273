import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("django_model_fsm").version
except pkg_resources.DistributionNotFound:
    __version__ = "not-packaged"


__all__ = [
    "__version__",
]
