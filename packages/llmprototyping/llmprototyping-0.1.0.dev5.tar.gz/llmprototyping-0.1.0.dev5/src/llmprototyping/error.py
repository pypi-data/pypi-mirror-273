
class LLMPException(Exception):
    def __init__(self, error_type, info, retryable, extra_data=None):
        Exception.__init__(self)

        self.error_type = error_type
        self.info = info
        self.retryable = retryable
        self.extra_data = extra_data

    def __str__(self) -> str:
        return f"LLMPException {self.error_type} ({'retryable' if self.retryable else 'final'}) {self.info}"

    @staticmethod
    def not_available(info):
        return LLMPException("not available", info, True)
    @staticmethod
    def unknown_backend(info):
        return LLMPException("unknown backend", info, False)
    @staticmethod
    def timeout(info):
        return LLMPException("timeout", info, True)   
    @staticmethod
    def service_error(info, retryable):
        return LLMPException("service error", info, retryable == True)   
    @staticmethod
    def param_error(info):
        return LLMPException("error with parameter", info, False)
    @staticmethod
    def not_found(info):
        return LLMPException("not found", info, False)
    @staticmethod
    def database_error(info):
        return LLMPException("docdb error", info, False)