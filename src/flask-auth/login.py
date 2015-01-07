from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):
    username = TextField('Netid', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])

    def __init__(self, get_user_func, *args, **kwargs):
        print("setting up form")
        Form.__init__(self, *args, **kwargs)
        self.user = None
        self.get_user_func = get_user_func

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        fields = {}
        for field in self:
            fields[field.name] = field.data
        print(fields)

        (user, e) = self.get_user_func(fields)

        if e is not None:
            self.errors['username'] = e
            return False

        self.user = user
        return True
