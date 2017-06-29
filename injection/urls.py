from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_request, name='login_request'),
    url(r'^logout$', views.logout_request, name='logout_request'),
    url(r'^submit/(?P<session_id>[0-9]+)$', views.submit, name='submit'),
    url(r'^reset_session/(?P<session_id>[0-9]+)$', views.reset_session, name='reset_session'),
]