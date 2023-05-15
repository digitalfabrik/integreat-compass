import logging

from django.contrib.auth.views import redirect_to_login
from django.urls import resolve

from ...cms.constants import namespaces

logger = logging.getLogger(__name__)


# pylint: disable=too-few-public-methods
class AccessControlMiddleware:
    """
    Middleware class that performs a basic access control. For urls that are whitelisted (see
    :attr:`~integreat_compass.core.middleware.access_control_middleware.AccessControlMiddleware.whitelist`), no additional
    rules are enforced.
    For all other urls, the user has to be logged in.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware for the current view

        :param get_response: A callable to get the response for the current request
        :type get_response: ~collections.abc.Callable
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Call the middleware for the current request

        :param request: Django request
        :type request: ~django.http.HttpRequest

        :return: The response after the region has been added to the request variable
        :rtype: ~django.http.HttpResponse
        """
        resolver_match = resolve(request.path)
        if (
            namespaces.PUBLIC not in resolver_match.namespaces
            and not request.user.is_authenticated
        ):
            return redirect_to_login(request.path)
        return self.get_response(request)
