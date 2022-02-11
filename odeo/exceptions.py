class GeneralError(Exception):
    error_code: int = 10000


class InputValidationError(Exception):
    error_code: int = 10001


class InsufficientBalanceError(Exception):
    error_code: int = 40011


class InvalidBankError(Exception):
    error_code: int = 40002


class ResourceNotFoundError(Exception):
    error_code: int = 20002
