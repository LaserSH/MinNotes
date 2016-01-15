from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.NotebookView.as_view(),
            name='notebook'),
    url(r'^(?P<notebook_id>[0-9]+)/(?P<note_id>[0-9]+)/$',
            views.note_view, name='note'),
    url(r'^(?P<notebook_id>[0-9]+)/(?P<note_id>[0-9]+)/edit/$',
            views.note_edit, name='edit'),
]
