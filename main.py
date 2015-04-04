#!/usr/bin/env python

from flask import Flask, request, redirect, url_for, make_response
import functools

class CustomFlask(Flask):

    def _logged_in(self):
        return request.args.get('auth') is not None

    def _login_required(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self._logged_in():
                return make_response('Unauthorized', 401)
            return func(*args, **kwargs)
        return wrapper

    def _with_auth(self, viewfunc, public):
        if public is True:
            return viewfunc
        else:
            return self._login_required(viewfunc)

    def route(self, rule, **options):
        def decorator(f):
            is_public = options.pop('public', False)
            protected_f = self._with_auth(f, is_public)
            return Flask.route(self, rule, **options)(protected_f)
        return decorator

app = CustomFlask(__name__)


@app.route('/open', public=True)
def hello_world():
    return 'Hello World!'

@app.route('/closed')
def goodbye_world():
    return "You're in! Good job"

if __name__ == '__main__':
    app.run(debug = True)
