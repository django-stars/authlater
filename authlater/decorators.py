try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps
    # Python 2.3, 2.4 fallback.
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from authlater.utils import save_interrupted_views_func, is_ajax_request


AJAX_REQUEST_CHECK = getattr(
    settings, 'AJAX_REQUEST_CHECK_FUNCTION', is_ajax_request
)


def user_passes_test(
    test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME,
    message="Log in to proceed", is_ajax=AJAX_REQUEST_CHECK,
    ajax_redirect_template_name="passive_auth/ajax_redirect.html"
):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    if not login_url:
        login_url = settings.LOGIN_URL

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            messages.info(request, message)
            save_interrupted_views_func(view_func, request, args, kwargs)
            redirect_url = login_url
            if is_ajax(request):
                return render_to_response(
                    ajax_redirect_template_name,
                    {'redirect_url':redirect_url},
                    mimetype='application/json',
                    context_instance=RequestContext(request),
                )
            else:
                return HttpResponseRedirect(redirect_url)
        return wraps(view_func)(_wrapped_view)
    return decorator


def login_required_on_post(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME,
    login_url=None, message="Log in to proceed"
):
    """
    Decorator for views that checks that the user is logged in when using POST,
    redirecting to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda r: r.method != "POST" or r.user.is_authenticated(),
        login_url=login_url, redirect_field_name=redirect_field_name,
        message=message
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
