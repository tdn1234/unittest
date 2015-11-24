from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views


urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'myblog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^$', views.HomeView.as_view(), name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^blog/', include('blog.urls')),
                       )
