def notimplemented(func):
    func.__isnotimplemented__ = True
    return func


def isnotimplemented(func):
    return getattr(func, "__isnotimplemented__", False)


def isimplemented(func):
    return not isnotimplemented(func)
