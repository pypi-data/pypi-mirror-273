import json
import inspect
import logging
import functools
from zenutils import importutils
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .exceptions import JsonPayloadDecodeError
from .exceptions import RequestMethodNotAllowed
from .settings import DJANGO_APIS_ALLOWED_METHODS
from .settings import DJANGO_APIS_APIVIEW
from .settings import DJANGO_APIS_ENABLE_REQUEST_LOG
from .settings import DJANGO_APIS_REQUEST_LOG_NAME
from .response import SimpleJsonResponsePackage
from .utils import get_time_string
from .utils import get_request_headers
from .utils import get_request_log_text


class Apiview(object):
    def __init__(
        self,
        default_methods=None,
        response_package_class=None,
        enable_request_log=None,
        request_log_logger_name=None,
        request_log_level=logging.INFO,
    ):
        # 默认允许的请求类型
        if default_methods is None:
            default_methods = DJANGO_APIS_ALLOWED_METHODS
        self.default_methods = default_methods
        # 响应数据封装类
        if response_package_class is None:
            response_package_class = SimpleJsonResponsePackage
        self.response_package_class = response_package_class
        # 是否记录请求日志
        if enable_request_log is None:
            enable_request_log = DJANGO_APIS_ENABLE_REQUEST_LOG
        self.enable_request_log = enable_request_log
        # 请求日志名称
        if request_log_logger_name is None:
            request_log_logger_name = DJANGO_APIS_REQUEST_LOG_NAME
        self.request_log_logger_name = request_log_logger_name
        # 请求日志级别
        self.request_log_level = request_log_level
        # 请求日志管理器
        self.logger = logging.getLogger(self.request_log_logger_name or __name__)

    def get_methods(self, methods):
        """获取当前请求支持的请求类型。"""
        if methods is None:
            return self.default_methods
        if isinstance(methods, str):
            return [methods.upper()]
        return [x.upper() for x in methods]

    def get_request_log(self, request, response_data):
        """Access日志内容。"""
        return {
            "time": get_time_string(),
            "method": request.method,
            "path": request.path,
            "params": dict(request.GET),
            "body": get_request_log_text(request.body),
            "response": response_data,
            "headers": get_request_headers(request),
        }

    def write_request_log(self, request, response_data):
        """记录Access日志。"""
        if self.enable_request_log:
            self.logger.log(
                self.request_log_level,
                json.dumps(
                    self.get_request_log(request, response_data),
                    ensure_ascii=False,
                ),
            )

    def __call__(self, methods=None):
        """接口视图注解。"""
        methods = self.get_methods(methods)

        def outer(real_view_func):
            @functools.wraps(real_view_func)
            def inner(request, *args, **kwargs):
                try:
                    # 检查请求类型
                    if request.method not in methods:
                        raise RequestMethodNotAllowed()
                    # 执行实际的视图
                    result = real_view_func(request, *args, **kwargs)
                    error = None
                    success = True
                except Exception as err:
                    result = None
                    error = err
                    success = False
                if isinstance(result, HttpResponse):
                    # 已经是完整的响应体
                    response = result
                    # @todo: 需要进一步检查是否安全
                    response_data = get_request_log_text(response.content)
                else:
                    # 结果封装和返回
                    response_data = self.response_package_class(
                        result, error, success
                    ).pack()
                    response = JsonResponse(
                        response_data,
                        json_dumps_params={
                            "ensure_ascii": False,
                        },
                    )
                self.write_request_log(request, response_data)
                return response

            return csrf_exempt(inner)

        return outer


# 默认的apiview注解。
apiview = Apiview()


def get_json_payload(request):
    """解析json请求体。"""
    try:
        if not request.body:
            return {}
        else:
            return json.loads(request.body)
    except Exception:
        raise JsonPayloadDecodeError()


def get_cookie(request, cookie_name, default=None):
    """提取cookie值。"""
    return request.COOKIES.get(cookie_name, default)


def get_apiview():
    """获取应用默认的apiview注解。"""
    if DJANGO_APIS_APIVIEW:
        return importutils.import_from_string(DJANGO_APIS_APIVIEW)
    else:
        return apiview
