class AppError(Exception):
    pass


class AuthError(AppError):
    pass


class UserAlreadyExists(AppError):
    pass

class ForbiddenNotificationAccess(Exception):
    pass
