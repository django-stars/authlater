from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^account/login/', 'authlater.views.login', name='auth-login'),
    url(r'^account/logout/', 'django.contrib.auth.views.logout', name='auth-logout'),
    url(r'^form/', 'testapp.views.view_with_form', name='form'),
    url(r'^', 'testapp.views.homepage', name='homepage')
)
