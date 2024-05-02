from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return render(request, 'index/index.html', context={
            "index": 0
        })
    else:
        return redirect('/home/')


def contact(request):
    if not request.user.is_authenticated:
        return render(request, 'index/contact.html', context={
            "index": 1
        })
    else:
        return redirect('/home/')


def why_me(request):
    if not request.user.is_authenticated:
        return render(request, 'index/index.html', context={
            "index": 2
        })
    else:
        return redirect('/home/')

def pricing(request):
    if not request.user.is_authenticated:
        return render(request, 'index/pricing.html', context={
            "index": 3
        })
    else:
        return redirect('/home/')