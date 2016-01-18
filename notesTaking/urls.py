from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new_notebook/$', views.notebook_new, name="notebook_new"),
    url(r'^(?P<slug>[\w\-]+)/$', views.NotebookView.as_view(),
            name='notebook'),
    url(r'^(?P<slug>[\w\-]+)/new_note/$', views.note_new, name="note_new"),
    url(r'^(?P<slug1>[\w\-]+)/(?P<slug2>[\w\-]+)/$',
            views.note_view, name='note'),
    url(r'^(?P<slug1>[\w\-]+)/(?P<slug2>[\w\-]+)/edit/$',
            views.note_edit, name='edit'),
]
