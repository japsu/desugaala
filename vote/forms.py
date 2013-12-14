# encoding: utf-8
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Button, Div
from crispy_forms.bootstrap import FormActions, StrictButton

class LoginForm(forms.Form):
  username = forms.CharField(label=u'Käyttäjänimi')
  password = forms.CharField(label=u'Salasana', widget=forms.PasswordInput)

  def __init__(self, *args, **kwargs):
    super(LoginForm, self).__init__(*args, **kwargs)

    self.helper = FormHelper()
    self.helper.form_id = 'login-form'
    self.helper.form_class = 'form-horizontal'
    self.helper.label_class = 'col-md-2'
    self.helper.field_class = 'col-md-4'
    self.helper.layout = Layout(
        'username',
        'password',

        # XXX ugly
        Div(
          Div(
            StrictButton(u'Kirjaudu sisään', css_class='btn-primary', css_id='login-button'),
            css_class='controls col-md-2 col-md-offset-2'
          ),
          css_class='form-group'
        )
    )
