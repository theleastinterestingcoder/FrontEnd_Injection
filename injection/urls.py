from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_request, name='login_request'),
    url(r'^create_user$', views.create_user, name='create_user'),
    url(r'^logout$', views.logout_request, name='logout_request'),
    url(r'^submit/(?P<session_id>[0-9]+)/(?P<leaderboard_id>[0-9]+)$', views.view_session, name='view_session'),
    url(r'^my_session$', views.my_session, name='my_session'),
    url(r'^reset_session/(?P<session_id>[0-9]+)$', views.reset_session, name='reset_session'),
]