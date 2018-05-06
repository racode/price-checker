__author__ = "esobolie"


class UserError(Exception):
    def ___init__(self, message):
        self.message = message


class UserNotExistsError(UserError):
    pass


class IncorrectPasswordError(UserError):
    pass


class UserAlreadyRegistered(UserError):
    pass


class InvalidEmailError(UserError):
    pass
