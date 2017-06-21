from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^submit/(?P<session_id>[0-9]+)$', views.submit, name='submit'),
    url(r'^reset_session/(?P<session_id>[0-9]+)$', views.reset_session, name='reset_session'),
]