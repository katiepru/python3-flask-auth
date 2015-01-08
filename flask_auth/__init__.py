from flask_auth.ldap import LDAP
from flask_auth.login import LoginForm
from flask_login import login_user

class Auth:

    def __init__(self, config, query_func, register_func=None):
        valid_methods = [ "local", "ldap"]
        for method in config['methods']:
            if method not in valid_methods:
                raise AttributeError("Method %s not defined" % method)
        self.methods = config['methods']
        self.ldap_config = config['ldap']
        self.query_func = query_func
        self.register_func = register_func

    def login(self, request, showLogin, nextAction):
        form = LoginForm(self.getUserFunc, request.form)
        if request.method == 'POST' and form.validate():
            return nextAction(form.user)
        return showLogin(form=form)

    def getUserFunc(self, fields):
        """Go through each method for authentication and see if we find a
        match. This is done in the order they were specified by the user. First
        one to find a match succeeds"""

        user = None

        for method in self.methods:

            if method == "local":
                user = self.query_func(fields)
                if user is None:
                    continue
                break

            if method == "ldap":
                ldap_obj = LDAP(self.ldap_config)
                (res, e) = ldap_obj.authenticate(fields['username'],
                    fields['password'])
                if not res:
                    continue
                user = self.query_func(fields)
                if user is None:
                    if self.register_func is None:
                        continue
                    user = self.register_func(fields)
                    if user is None:
                        continue
                    break

        if not user is None:
            login_user(user)
            return (user, None)
        return (None, "Invalid credentials")
