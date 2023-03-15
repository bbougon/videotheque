class RunnerException(Exception):
    def __init__(
        self, msg: str, return_code: int, stderr: bytes, *args, **kwargs
    ) -> None:
        super().__init__(*args)
        self.msg = msg
        self.details = {
            "return_code": return_code,
            "args": ",".join([v for k, v in kwargs.items()]),
            "stderr": stderr.decode("utf-8"),
        }
