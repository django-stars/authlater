authlater
=========

Authlater adds ability for non-authinticated users to post forms and only then login. When user logs in, form will be posted if it's valid, or prepopulated form with error will be showed in other case.

Installation
------------

Installing form github: `pip install -e git://github.com/equeny/authlater.git#egg=authlater`

Installing from source: `git clone git://github.com/equeny/authlater.git; cd asyncmongo; python setup.py install`

Usage
-----

    # views.py
    from authlater.decorators import login_required_on_post

    @login_required_on_post
    def some_view(request):
        # some code ...


    # urls.py
    url(r'^account/login/', 'authlater.views.login', name='auth-login'),


    # settings.py
    LOGIN_URL = '/account/login/'

Examples

    See testproject in current repo for more info

Requirements
------------
The following python libraries are required

* [django>=1.2](http://www.djangoproject.com/download/)

Issues
------

Please report any issues via [github issues](https://github.com/equeny/authlater/issues)
