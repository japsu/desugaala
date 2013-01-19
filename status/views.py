from django.shortcuts import render

from .models import Watch, Category

def status_page(request):
    categories = []

    for category in Category.objects.all():
        result = category.evaluate()
        categories.append((category, result.get('winner'), result.get('tied_winners')))

    vars = dict(
        watches=Watch.objects.all(),
        categories=categories
    )

    return render(request, 'status.jade', vars)