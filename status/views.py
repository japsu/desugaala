import datetime

from django.shortcuts import render
from django.views.decorators.cache import cache_page

from vote.models import Category, Ballot
from .models import Watch

@cache_page(5 * 60)
def status_page(request):
    categories = []

    for category in Category.objects.all():
        result = category.evaluate()
        num_votes = category.ballotcategory_set.all().count()
        categories.append((category, result.get('winner'), result.get('tied_winners'), num_votes))

    vars = dict(
        timestamp=datetime.datetime.now(),
        num_votes=Ballot.objects.all().count(),
        watches=Watch.objects.all(),
        categories=categories
    )

    return render(request, 'status.jade', vars)