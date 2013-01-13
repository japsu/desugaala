import datetime
from random import shuffle

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie


from .models import Category
from .forms import LoginForm
from .helpers import json_rest, throttle_post

if getattr(settings, 'DEMO_MODE', False):
  perform_checks = _fake_perform_checks
else:
  from phpbb.auth.auth_db import login_db
  perform_checks = _actual_perform_checks

def _fake_perform_checks(func):
  @wraps(func)
  def inner(request, data, *args, **kwargs):
    if data['username'] == 'onjo' and data['password'] == 'aanestetty':
      return dict(result='already_voted')

    elif data['username'] == 'desu' and data['password'] == 'salainen':
      user_row = dict(user_id=1)
      return func(request, data, user_row, *args, **kwargs)

    else:
      return dict(result='login_failed')

def _actual_perform_checks(func):
  @wraps(func)
  def inner(request, data, *args, **kwargs):
    result, user_row = login_db(data['username'], data['password'])
    if not result == 'LOGIN_SUCCESS':
      return dict(result='login_failed')

    if AlreadyVoted.objects.filter(user_id=user_row['user_id']).exists():
      return dict(result='already_voted')

    return func(request, data, user_row, *args, **kwargs)

  return inner

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
@perform_checks
def login_api(request, data, user_row):
  return dict(result='ok')

@throttle_post
@json_rest
@perform_checks
@handle_errors
def vote_api(request, data, user_row):
  timestamp = datetime.utcnow()

  # mark user as already voted
  already_voted = AlreadyVoted(
    user_id=user_row['user_id'],
    ip_address=request.META['REMOTE_ADDR'],
    user_agent=request.META['HTTP_USER_AGENT'],
    timestamp=timestamp
  )

  ballot = Ballot(
    ip_address=request.META['REMOTE_ADDR'],
    user_agent=request.META['HTTP_USER_AGENT'],
    timestamp=timestamp
  )

  ballot_categories = []

  for categoryId, optionIds in data['ballot'].iteritems():
    # check that category exists
    category = Category.objects.get(id=int(categoryId))
    ballot_category = BallotCategory(category=category)
    ballot_options = []

    # check that every option only occurs once
    optionIds = [int(optionId) for optionId in optionIds]
    if set(optionIds).length != optionIds.length:
      raise ValueError('forged ballot with duplicate ids')

    for index, optionId in enumerate(optionIds):
      # check that options belong to this category
      option = Option.objects.get(id=optionId, category=category)

      ballot_options.append(BallotOption(
        order=index,
        option=option
      ))

    ballot_categories.append((ballot_category, ballot_options))

  # all checks passed, commit

  already_voted.save()
  ballot.save()

  for ballot_category, ballot_options in ballot_categories:
    ballot_category.ballot = ballot
    ballot_category.save()

    for ballot_option in ballot_options:
      ballot_option.ballot_category = ballot_category
      ballot_option.save()

  return dict(result='ok')

