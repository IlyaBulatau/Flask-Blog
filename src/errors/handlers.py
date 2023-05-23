from errors import errors

def not_found(e):
    return errors.NotFoundError()

def server_error(e):
    return errors.ServerError()