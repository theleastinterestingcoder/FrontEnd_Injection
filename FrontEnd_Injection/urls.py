from django.conf.urls import include, url
from django.contrib import admin
from injection import views

urlpatterns = [
    url(r'^injection/', include('injection.urls')),
    url('^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
]
