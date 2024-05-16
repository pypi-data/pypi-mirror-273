class ResponsePackage(object):
    def __init__(self, result, error, success=None):
        """
        @parameter: result Any, 返回数据
        @parameter: error Exception, 异常
        @parameter: success bool, 表示返回正常还是异常。
            如果success为None，则error不为空，则异常。
        """
        self.result = result
        self.error = error
        self.success = success
        if self.success is None:
            if self.error is None:
                self.success = True
            else:
                self.success = False

    def pack(self):
        if self.success:
            return self.pack_success()
        else:
            return self.pack_error()

    def pack_success(self):
        raise NotImplementedError()

    def pack_error(self):
        return NotImplementedError()

    def parse_error(self):
        if hasattr(self.error, "json"):
            info = self.error.json()
            if "code" in info and "message" in info:
                return info["code"], info["message"]
            else:
                return -1, str(self.error)
        args = self.error.args
        if isinstance(args, tuple) and len(args) >= 2:
            code = args[0]
            message = args[1]
            return code, message
        return -1, str(self.error)


class SimpleJsonResponsePackage(ResponsePackage):
    """
    简易的Json响应体封装。主要有以下字段：

        success: bool
        msg: string
        code: int
        data: any

    success表示业务是否成功处理。
    msg表示业务处理异常时的错误信息。如果业务成功处理，则返回常量OK。
    code表示业务处理异常时的错误码。如果业务成功处理，则返回常量0。
    data表示业务数据。
    """

    def pack_success(self):
        return {
            "success": True,
            "msg": "OK",
            "code": 0,
            "data": self.result,
        }

    def pack_error(self):
        code, msg = self.parse_error()
        return {
            "success": False,
            "msg": msg,
            "code": code,
            "data": None,
        }
