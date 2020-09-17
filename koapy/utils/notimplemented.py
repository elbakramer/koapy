def notimplemented(func):
    func.__isnotimplemented__ = True
    return func

def isnotimplemented(func):
    return getattr(func, '__isnotimplented__', False)

def isimplemented(func):
    return not isnotimplemented(func)
    