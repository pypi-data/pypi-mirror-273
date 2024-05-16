class ValidationError(RuntimeError):
    """请求参数验证失败。"""

    def __init__(self, form):
        self.form = form

    def json(self):
        messages = []
        for field_name, errors in self.form.errors.as_data().items():
            infos = []
            for error in errors:
                if error.message:
                    message = str(error.message)
                    if message not in infos:
                        infos.append(message)
                for message in error.messages:
                    message = str(message)
                    if message not in infos:
                        infos.append(message)
            message = "".join(infos)
            messages.append(f"{field_name}: {message}")
        return {
            "code": 11,
            "message": "\n".join(messages),
        }


class JsonPayloadDecodeError(RuntimeError):
    args = (12, "请求体不是有效的json格式，无法正常解析。")


class RequestMethodNotAllowed(RuntimeError):
    args = (13, "不允许的HTTP请求类型。")


class SystemError(RuntimeError):
    args = (2, "系统开小差了，请联系管理员或稍候再试 ^_^")
