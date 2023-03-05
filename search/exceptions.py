class RunnerException(Exception):
    def __init__(
        self, msg: str, return_code: int, stderr: bytes, *args: object
    ) -> None:
        super().__init__(*args)
        self.msg = msg
        self.details = {
            "return_code": return_code,
            "args": ",".join(args),
            "stderr": stderr.decode("utf-8"),
        }
