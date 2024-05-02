from django.shortcuts import redirect
from django.urls import reverse


class PreventLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login') and request.user.is_authenticated:
            return redirect('/')
        return self.get_response(request)
