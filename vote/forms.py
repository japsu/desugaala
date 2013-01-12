# encoding: utf-8

from django import forms

class LoginForm(forms.Form):
  username = forms.CharField(label=u'Käyttäjänimi')
  password = forms.CharField(label=u'Salasana', widget=forms.PasswordInput)