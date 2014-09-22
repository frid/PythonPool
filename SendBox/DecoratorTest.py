from ipdb import set_trace

def logged(func):
    def with_logging(*args, **kwargs):
        print func.__name__ + " was called "
        return func(*args, **kwargs)
    return with_logging

def logged2(func):
    def logfun(*args, **kwargs):
        set_trace()
        print 'logged2 is called'
        return func(*args, **kwargs)
    return logfun

@logged
@logged2
def f(x):
    return x**x



print(f(2))
