from django.http import HttpResponseRedirect
from django.contrib.auth.views import login as django_login
from utils import get_interrupted_view_func, run_interrupted_view_func

def login(request, original_login_view=django_login, *args, **kwargs):
    """
    Wrap default login function. After user logs in, 
    we check if there is saved request data. And if it is, 
    we emulate this request
    """

    django_login_response = original_login_view(request, *args, **kwargs)
    if isinstance(django_login_response, HttpResponseRedirect) \
    and get_interrupted_view_func(request):
        return run_interrupted_view_func(request)
    else: 
        return django_login_response
