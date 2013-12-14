import datetime
from random import shuffle
from functools import wraps

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.timezone import utc
from django.template.loader import render_to_string

from .models import Category, Option, Ballot, BallotCategory, BallotOption, AlreadyVoted
from .forms import LoginForm
from .helpers import json_rest, throttle_post

DEMO_MODE = getattr(settings, 'DEMO_MODE', False)
DESUGAALA_TEMPLATE_PACK = getattr(settings, 'DESUGAALA_TEMPLATE_PACK', 'desugaala')

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

  return inner

def login_db_with_retry(username, password):
  try:
    return login_db(username, password)
  except OperationalError:
    connect_to_database()
    return login_db(username, password)

def _actual_perform_checks(func):
  @wraps(func)
  def inner(request, data, *args, **kwargs):
    result, user_row = login_db_with_retry(data['username'], data['password'])
    if result != 'LOGIN_SUCCESS':
      return dict(result='login_failed')

    if AlreadyVoted.objects.filter(user_id=user_row['user_id']).exists():
      return dict(result='already_voted')

    return func(request, data, user_row, *args, **kwargs)

  return inner

if DEMO_MODE:
  perform_checks = _fake_perform_checks
else:
  from phpbb.auth.auth_db import login_db
  from phpbb.auth.backends import connect_to_database
  from MySQLdb import OperationalError # XXX
  perform_checks = _actual_perform_checks
  connect_to_database()

def handle_errors(func):
  # XXX stub
  return func

def render_from_pack_to_string(template_name, *args, **kwargs):
  template_name = "{pack}/{template_name}".format(
    pack=DESUGAALA_TEMPLATE_PACK,
    template_name=template_name
  )

  return render_to_string(template_name, *args, **kwargs)

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
      login_form=LoginForm(),
      jumbotron=render_from_pack_to_string('jumbotron.jade'),
      header=render_from_pack_to_string('header.jade'),
      credit=render_from_pack_to_string('credit.jade'),
      thanks=render_from_pack_to_string('thanks.jade'),
      DEMO_MODE=DEMO_MODE,
      DESUGAALA_TEMPLATE_PACK=DESUGAALA_TEMPLATE_PACK,
      GOOGLE_ANALYTICS_TOKEN=getattr(settings, 'GOOGLE_ANALYTICS_TOKEN', '')
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
  timestamp = datetime.datetime.utcnow().replace(tzinfo=utc)

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
    if len(set(optionIds)) != len(optionIds):
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

  if not DEMO_MODE:
    already_voted.save()

  ballot.save()

  for ballot_category, ballot_options in ballot_categories:
    ballot_category.ballot = ballot
    ballot_category.save()

    for ballot_option in ballot_options:
      ballot_option.ballot_category = ballot_category
      ballot_option.save()

  return dict(result='ok')

