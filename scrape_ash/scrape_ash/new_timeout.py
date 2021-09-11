import socket
from typing import Callable

from .monkeysocket import monkeyblocking

timeout_secs = 10

socket.setdefaulttimeout(timeout_secs)
socket.socket.setblocking = monkeyblocking()

sock = socket.socket()
sock.settimeout(timeout_secs)
sock.setblocking(True)  # keeps existing timeout


def dynamic_timeout(
    timeout_delta: float = 10.0,
):

    old_timeout = sock.gettimeout()

    if sock.gettimeout():
        if sock.gettimeout() < timeout_delta:
            timeout_secs = timeout_delta

    #     if type(old_timeout) is not float:
    #         timeout_secs = timeout_delta
    #
    #     else:

    timeout_secs = old_timeout
    timeout_secs += timeout_delta

    sock.settimeout(timeout_secs)
    print(f"Increasing timeout from {old_timeout} to {timeout_secs} seconds.")
