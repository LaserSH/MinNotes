from django.contrib import admin

from .models import Note, Notebook, UserProfile

class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'mod_date')
    fieldsets = [
        ('Date info', {'fields': ['init_date'], 'classes': 'collapse'}),
        ('Note', {'fields': ['notebook', 'title', 'content']}),
    ]

class NotebookAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'mod_date')
    fieldsets = [
        ('Date info', {'fields': ['init_date'], 'classes': 'collapse'}),
        ('Note', {'fields': ['title', 'description']}),
    ]

admin.site.register(Note, NoteAdmin)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(UserProfile)
