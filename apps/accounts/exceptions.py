

class UserEmailAlreadyExists(Exception):
    pass



class UserNameAlreadyExists(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class InactiveUser(Exception):
    pass


class InvalidCurrentPassword(Exception):
    pass


class PasswordsNotMatch(Exception):
    pass


class OldPasswordMatchNewPassword(Exception):
    pass