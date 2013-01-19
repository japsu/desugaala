import datetime

from django.shortcuts import render
from django.views.decorators.cache import cache_page

from vote.models import Category, Ballot
from .models import Watch

@cache_page(5 * 60)
def status_page(request):
    categories = []
    watches = []

    for category in Category.objects.all():
        result = category.evaluate()
        num_votes = category.ballotcategory_set.all().count()
        categories.append((category, result.get('winner'), result.get('tied_winners'), num_votes))

    for watch in Watch.objects.all():
        results = []
        num_category_votes = watch.category.ballotcategory_set.all().count()

        for option, num_option_votes in watch.evaluate():
          percentage = 100 * num_option_votes / num_category_votes
          results.append((option, num_option_votes, percentage))

        watches.append((watch.category, results))

    vars = dict(
        timestamp=datetime.datetime.now(),
        num_votes=Ballot.objects.all().count(),
        watches=watches,
        categories=categories
    )

    return render(request, 'status.jade', vars)