from django.conf import settings

# 接口如果不指定methods，则默认同时支持get和post请求
DJANGO_APIS_ALLOWED_METHODS = getattr(
    settings,
    "DJANGO_APIS_ALLOWED_METHODS",
    ["GET", "POST"],
)
# 获取应用默认的apiview函数
# 一般应用需要自定义接口返回数据格式
DJANGO_APIS_APIVIEW = getattr(
    settings,
    "DJANGO_APIS_APIVIEW",
    None,
)
# 记录完整的请求和响应信息
DJANGO_APIS_ENABLE_REQUEST_LOG = getattr(
    settings,
    "DJANGO_APIS_ENABLE_REQUEST_LOG",
    False,
)
DJANGO_APIS_REQUEST_LOG_NAME = getattr(
    settings,
    "DJANGO_APIS_REQUEST_LOG_NAME",
    None,
)
