from django.utils.importlib import import_module
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME


SAVE_REQUEST_VARIABLE = getattr(
    settings, 'AUTHLATER_SAVE_REQUEST_VARIABLE', 'last_saved_request'
)
DEFAULT_SKIP_PARAMS = getattr(
    settings, 'AUTHLATER_SKIP_PARAMS', ['csrfmiddlewaretoken']
)


class InterruptedViewFuncDoesNotExist(Exception):
    """No interrupted function found in session"""
    pass


class InterruptedViewFuncNotCallable(Exception):
    """Interrupted function is not callable"""
    pass


def save_interrupted_views_func(
    function, request, args, kwargs, skip_request_params=DEFAULT_SKIP_PARAMS
):
    """Saving data from request, so we can emulate this request in future"""

    # TODO rewrite this to save only minimal data
    get_params = request.GET.copy()
    post_params = request.POST.copy()
    for param in skip_request_params:
        try:
            del get_params[param]
        except KeyError:
            pass
        try:
            del post_params[param]
        except KeyError:
            pass

    request.session[SAVE_REQUEST_VARIABLE] = {
        "function_module": function.__module__,
        "function_name": function.__name__,
        "POST": post_params,
        "GET": get_params,
#        "META": request.META.copy(),
        "method": request.method,
        "args": args,
        "kwargs": kwargs,
    }


def get_interrupted_view_func(
    request, redirect_field_name=REDIRECT_FIELD_NAME
):
    return request.session.get(SAVE_REQUEST_VARIABLE, False)


def run_interrupted_view_func(request):

    func_data = get_interrupted_view_func(request)
    if not func_data:
        raise InterruptedViewFuncDoesNotExist()
    else:
        func = getattr(
            import_module(func_data['function_module']),
            func_data['function_name']
        )
        if not callable(func):
            raise InterruptedViewFuncNotCallable()
        new_request = request
        new_request.POST = func_data.get('POST')
        new_request.GET = func_data.get('GET')
#        new_request.META = func_data.get('META')
        new_request.method = func_data.get('method')
        return func(
            new_request, *func_data.get('args', []),
            **func_data.get('kwargs', {})
        )

def is_ajax_request(request):
    return request.is_ajax()
