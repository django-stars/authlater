from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.template import RequestContext

from authlater.decorators import login_required_on_post
from forms import SimpleForm


def homepage(request):
    return render_to_response(
        "homepage.html", context_instance=RequestContext(request)
    )


@login_required_on_post
def view_with_form(request):
    if request.method == 'POST':
        form = SimpleForm(request.POST)
        if form.is_valid():
            messages.info(request, 'Form has been successfully submited')
            return redirect('homepage')
    else:
        form = SimpleForm()

    return render_to_response("form.html", {
        'form': form,
    }, context_instance=RequestContext(request))
