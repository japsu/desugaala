from django.shortcuts import render

def vote_page(request):
    return render(request, 'vote.jade')