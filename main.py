#!/usr/bin/env python

from flask import Flask, request, redirect, url_for, make_response
import functools

app = Flask(__name__)


def logged_in():
    return request.args.get('auth') is not None

def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return make_response('Unauthorized', 401)
        return func(*args, **kwargs)
    return wrapper

def custom_route(rule, **options):
    def decorator(f):
        protected_f = None
        if options.pop('public', False) is True:
            protected_f = f
        else:
            protected_f = login_required(f)

        endpoint = options.pop('endpoint', None)
        app.add_url_rule(rule, endpoint, protected_f, **options)
        return protected_f
    return decorator


@custom_route('/open', public=True)
def hello_world():
    return 'Hello World!'

@custom_route('/closed')
def goodbye_world():
    return "You're in! Good job"

if __name__ == '__main__':
    app.run(debug = True)
