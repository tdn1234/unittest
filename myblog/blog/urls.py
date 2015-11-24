from django.conf.urls import url

from blog.views import EntryList, EntryDetail, EntryCreate


urlpatterns = [
    url(r'^list/$', EntryList.as_view()),
    url(r'^entry/(?P<pk>[0-9]+)/$', EntryDetail.as_view(), name='entry-detail'),
    url(r'^entry/create/$', EntryCreate.as_view(), name='entry-create'),
]
