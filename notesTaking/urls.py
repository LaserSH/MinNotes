from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new_notebook/$', views.notebook_new, name="notebook_new"),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<slug>[\w\-]+)/$', views.NotebookView.as_view(),
            name='notebook'),
    url(r'^(?P<slug>[\w\-]+)/new_note/$', views.note_new, name="note_new"),
    url(r'^(?P<slug1>[\w\-]+)/(?P<slug2>[\w\-]+)/$',
            views.note_view, name='note'),
    url(r'^(?P<slug1>[\w\-]+)/(?P<slug2>[\w\-]+)/edit/$',
            views.note_edit, name='edit'),
]
