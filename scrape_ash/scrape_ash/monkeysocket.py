import socket

# sometimes the timeout gets reset for no good reason
# this monkey patch fixes that, and is from:
# https://medium.com/pipedrive-engineering/socket-timeout-an-important-but-not-simple-issue-with-python-4bb3c58386b4


def monkeyblocking():
    setblocking_func = socket.socket.setblocking

    def wrapper(self, flag):
        if flag:
            # prohibit timeout reset
            timeout = socket.getdefaulttimeout()
            if timeout:
                self.settimeout(timeout)
            else:
                setblocking_func(self, flag)
        else:
            setblocking_func(self, flag)

    wrapper.__doc__ = setblocking_func.__doc__
    wrapper.__name__ = setblocking_func.__name__
    return wrapper
