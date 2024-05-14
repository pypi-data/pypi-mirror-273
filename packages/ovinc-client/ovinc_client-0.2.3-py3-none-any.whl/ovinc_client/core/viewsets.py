import traceback
from typing import Union

from django.conf import settings
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ovinc_client.core.cache import CacheMixin
from ovinc_client.core.logger import logger
from ovinc_client.core.models import RequestMock
from ovinc_client.core.utils import get_ip


class MainViewSet(CacheMixin, GenericViewSet):
    """
    Base ViewSet
    """

    enable_record_log = True

    def dispatch(self, request, *args, **kwargs):
        self.args = args  # pylint: disable=W0201
        self.kwargs = kwargs  # pylint: disable=W0201
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request  # pylint: disable=W0201
        self.headers = self.default_response_headers  # pylint: disable=W0201

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            # cache
            if self.enable_cache:
                has_cache, cache_data = self.get_cache(request, *args, **kwargs)
                # has cache, return directly
                if has_cache:
                    response = Response(cache_data)
                # no cache, perform request and set cache
                else:
                    response = handler(request, *args, **kwargs)
                    self.set_cache(response.data, request, *args, **kwargs)
            # no cache
            else:
                response = handler(request, *args, **kwargs)

        except Exception as exc:  # pylint: disable=W0718
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)  # pylint: disable=W0201

        # Record Disabled
        if not getattr(settings, "OVINC_API_RECORD_LOG", True) or not self.check_record_log(request, *args, **kwargs):
            return self.response

        # Record Request
        try:
            if hasattr(request, "user") and hasattr(request.user, "username") and hasattr(request.user, "nick_name"):
                user = f"{request.user.username}({request.user.nick_name})"
            elif hasattr(request, "user") and hasattr(request.user, "app_code") and hasattr(request.user, "app_name"):
                user = f"{request.user.app_code}({request.user.app_name})"
            else:
                user = str(getattr(request, "user", ""))
            logger.info(
                "[RequestLog] User => %s; Path => %s:%s; Request => %s; Response => %s; Extras => %s",
                user,
                request.method,
                request.path,
                {"params": request.query_params, "body": request.data},
                self.get_response_content(),
                {
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "ip": get_ip(request),
                    "referer": request.META.get("HTTP_REFERER", ""),
                },
            )

        except Exception:  # pylint: disable=W0718
            logger.error(traceback.format_exc())

        return self.response

    def check_record_log(self, request: Request, *args, **kwargs) -> bool:
        return self.enable_record_log

    def get_response_content(self) -> Union[str, dict, bytes]:
        if hasattr(self.response, "data"):
            return self.response.data
        if hasattr(self.response, "content"):
            return self.response.content
        if hasattr(self.response, "streaming_content"):
            return self.response.streaming_content
        msg = f"[RequestLogResponseContentNotSet] {self.response}"
        logger.warning(msg)
        return f"<{msg}>"

    @classmethod
    def call_action(cls, action: str, request: Request, params: dict = None, *args, **kwargs) -> Response:
        """
        call action directly
        """

        # request
        # pylint: disable=W0212
        _request = RequestMock(user=request.user, params=params or {}, request=request._request)

        # init
        view_set = cls()
        setattr(view_set, "request", _request)

        # call
        handler = getattr(cls, action)
        return handler(view_set, _request, *args, **kwargs).data


class CreateMixin(mixins.CreateModelMixin):
    ...


class ListMixin(mixins.ListModelMixin):
    ...


class RetrieveMixin(mixins.RetrieveModelMixin):
    ...


class UpdateMixin(mixins.UpdateModelMixin):
    ...


class DestroyMixin(mixins.DestroyModelMixin):
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()
