from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):

    def __init__(self, get_user_func, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.get_user_func = get_user_func
        self.errors = {}

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        fields = {}
        for field in self:
            fields[field.name] = field.data

        (user, e) = self.get_user_func(fields)

        if e is not None:
            self.errors['last_error'] = e
            return False

        self.user = user
        return True
