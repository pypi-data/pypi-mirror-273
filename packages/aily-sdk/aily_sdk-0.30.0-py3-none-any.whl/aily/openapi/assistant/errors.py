class AilyTimeoutError(Exception):
    """自定义的Timeout异常类"""

    def __init__(self, message=""):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"AilyTimeoutError: {self.message}"
