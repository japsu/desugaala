from django.shortcuts import render

from .models import Category
from .forms import LoginForm

def vote_page(request):
    vars = dict(
      categories=Category.objects.all(),
      login_form=LoginForm()
    )

    return render(request, 'vote.jade', vars)