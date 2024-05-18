class ActionOutOfContextError(Exception):
    pass


class PageNotLoadedError(Exception):
    pass


class MissingParametersError(Exception):
    pass


class NextButtonNotFoundError(Exception):
    pass


class ElementNotFoundError(Exception):
    pass


class UserNotFoundError(Exception):
    def __init__(self, username: str):
        self.username = username


class AccountLimitReachedError(Exception):
    def __init__(self, account: str):
        self.account: str = account
        super().__init__()


class LoginFailure(Exception):
    pass


class TargetsExhaustedError(Exception):
    pass


class NoAvailableAccountsError(Exception):
    pass
