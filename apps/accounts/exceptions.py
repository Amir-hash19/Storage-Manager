

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


class UserDoesNotExists(Exception):
    pass    



class InvalidResetPasswordToken(Exception):
    pass





class ResetPasswordTokenExpired(Exception):
    pass



class ResetPasswordTokenAlreadyUsed(Exception):
    pass