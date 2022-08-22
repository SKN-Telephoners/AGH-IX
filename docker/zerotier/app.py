import functools
import os

from flask import Flask, request, abort, Response
from flask_executor import Executor
from flask_httpauth import HTTPBasicAuth
from flask_shell2http import Shell2HTTP

network_api_key = str(
    open("/var/lib/zerotier-one/network.secret", "r").read().split("\n", 1)[0]
)

users = {
    "aghix": network_api_key,
}

app = Flask(__name__)
auth = HTTPBasicAuth()


def logging_decorator(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        print("*" * 64)
        print(
            "from logging_decorator: " + request.url + " : " + str(request.remote_addr)
        )
        print("*" * 64)
        return f(*args, **kwargs)

    return decorator


def login_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        user = verify_login()
        if user not in users:
            abort(Response("You are not logged in.", 401))
        return f(*args, **kwargs)

    return decorator


executor = Executor(app)
shell2http = Shell2HTTP(app=app, executor=executor, base_url_prefix="/commands/")


@auth.verify_password
def verify_password(username, password):
    if username in users and users.get(username, password):
        return username


@auth.login_required
def verify_login():
    return auth.username()


shell2http.register_command(
    endpoint="brctl",
    command_name="brctl",
    decorators=[login_required, logging_decorator],
)
shell2http.register_command(
    endpoint="ifconfig",
    command_name="ifconfig",
    decorators=[login_required, logging_decorator],
)
shell2http.register_command(
    endpoint="zerotier",
    command_name="zerotier-cli",
    decorators=[login_required, logging_decorator],
)
shell2http.register_command(
    endpoint="zerotierone",
    command_name="zerotier-one -d",
    decorators=[login_required, logging_decorator],
)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
