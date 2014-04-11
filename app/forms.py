from flaskext.wtf import Form, SubmitField, TextField, PasswordField, Required

class SignInForm(Form):
    """Just a simple signin form."""
    username = TextField('Username', validators=[Required()])
    api_key = TextField('API Key', validators=[Required()])