from django.contrib import admin

from .models import Note, Notebook

admin.site.register(Note)
admin.site.register(Notebook)
