from random import shuffle

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Category
from .forms import LoginForm
from .helpers import json_rest, throttle_post

@ensure_csrf_cookie
def vote_page(request):
    categories = Category.objects.all()
    options = []
    for category in categories:
      categoryOptions = list(category.option_set.all())
      shuffle(categoryOptions)
      options.append(categoryOptions)

    vars = dict(
      categories_options=zip(categories, options),
      login_form=LoginForm()
    )

    return render(request, 'vote.jade', vars)

@throttle_post
@json_rest
def login_api(request, data):
  return dict(
    result='ok' if data['username'] == 'desu' and data['password'] == 'salainen' else 'fail'
  )

@throttle_post
@json_rest
def vote_api(request, data):
  pass