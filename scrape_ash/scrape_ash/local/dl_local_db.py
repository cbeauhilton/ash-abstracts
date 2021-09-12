import os
import socket
from typing import List

from deta import Deta
from sqlite_utils import Database
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt

# from ..new_timeout import dynamic_timeout

project_id = os.environ.get("DETA_ID_ASH")
API_key = os.environ.get("DETA_TOKEN_ASH")
deta = Deta(API_key)


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

    timeout_secs = old_timeout
    timeout_secs += timeout_delta

    sock.settimeout(timeout_secs)
    print(f"Increasing timeout from {old_timeout} to {timeout_secs} seconds.")


@retry(
    retry=retry_if_exception_type(socket.timeout),
    before=dynamic_timeout(20),
    after=dynamic_timeout(20),
    stop=stop_after_attempt(500),
)
def deta_get_scraped_doi() -> List[str]:
    db_name = "abstracts"
    query = {"is_scraped": "1"}
    db = deta.Base(db_name)

    grab = db.fetch(query=query)
    response = grab.items
    while grab.last:
        grab = db.fetch(query=query, last=grab.last, limit=1000)
        response += grab.items
        print(len(response))

    print(response)
    print(f"Total number of scraped abstracts: {len(response)}")

    # return abstracts
    return response


abstracts = deta_get_scraped_doi()

for abstract in abstracts:
    abstract["latitude"] = abstract.pop("first_author_latitude")
    abstract["latitude"] = abstract.pop("first_author_longitude")

db = Database("../data/base.db", recreate=True)
db["base"].insert_all(abstracts, alter=True, pk="key")
