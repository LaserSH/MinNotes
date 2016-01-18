from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Notebook, Note

class IndexView(generic.ListView):
    template_name = "notesTaking/index.html"
    context_object_name = "notebook_list"

    def get_queryset(self):
        return Notebook.objects.order_by('-mod_date')[:5]

class NotebookView(generic.DetailView):
    model = Notebook
    template_name = "notesTaking/nb_view.html"

def index(request):
    notebook_list = Notebook.objects.order_by('-mod_date')[:5]
    context = {
        'notebook_list': notebook_list,
    }
    return render(request, 'notesTaking/index.html', context)

def notebook_view(request, notebook_id):
    nb = get_object_or_404(Notebook, pk = notebook_id)
    return render(request, 'notesTaking/nb_view.html', {'notebook': nb})

def note_view(request, slug1, slug2):
    nb = get_object_or_404(Notebook, slug = slug1)
    note = get_object_or_404(Note, slug = slug2)
    context = {
        'notebook': nb,
        'note': note,
    }
    return render(request, 'notesTaking/note_view.html', context)

def note_edit(request, slug1, slug2):
    nb = get_object_or_404(Notebook, slug = slug1)
    note = get_object_or_404(Note, slug = slug2)
    new_title = request.POST['title']
    new_content = request.POST['content']
    note.title = new_title
    note.content = new_content
    note.save()
    return HttpResponseRedirect(reverse('notesTaking:note',
            args=(slug1, slug2)))
