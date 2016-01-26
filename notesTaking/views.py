from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import generic


from .models import Notebook, Note
from .forms import NotebookForm, NoteForm, UserForm, UserProfileForm

from datetime import datetime

class IndexView(generic.ListView):
    template_name = "notesTaking/index.html"
    context_object_name = "notebook_list"

    def get_queryset(self):
        return Notebook.objects.order_by('-mod_date')[:5]

class NotebookView(generic.DetailView):
    model = Notebook
    template_name = "notesTaking/nb_view.html"

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('notesTaking:index'))

    return render(request, 'notesTaking/home.html')

@login_required
def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    context = {}
    notebook_list = notebook_list = Notebook.objects.filter(user=request.user.id)
    if (notebook_list is not None):
        context['notebook_list'] = notebook_list
    return render(request, 'notesTaking/index.html', context)

@login_required
def notebook_view(request, slug):
    nb = get_object_or_404(Notebook, slug = slug)
    return render(request, 'notesTaking/nb_view.html', {'notebook': nb})

@login_required
def note_view(request, slug1, slug2):
    nb = get_object_or_404(Notebook, slug = slug1)
    note = get_object_or_404(Note, slug = slug2)
    context = {
        'notebook': nb,
        'note': note,
    }
    return render(request, 'notesTaking/note_view.html', context)

@login_required
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

@login_required
def notebook_new(request):
    if request.method == 'POST':
        form = NotebookForm(request.POST)

        if form.is_valid():
            nb = form.save(commit=False)
            nb.init_date = datetime.now()
            nb.user = request.user
            nb.save()
            return index(request)

        else:
            print(form.errors)

    # If the request was not a POST, display the form to enter details.
    else:
        form = NotebookForm(auto_id=True)

    return render(request, 'notesTaking/notebook_new.html', {'form': form} )

@login_required
def note_new(request, slug):
    nb = get_object_or_404(Notebook, slug = slug)

    if request.method == 'POST':
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.notebook = nb
            note.init_date = datetime.now()
            note.save()
            return render(request, 'notesTaking/nb_view.html', {'notebook': nb})

        else:
            print(form.errors)
    else:
        form = NoteForm(auto_id=True)

    return render(request, 'notesTaking/note_new.html', {'form': form, 'notebook': nb})

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'notesTaking/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('notesTaking:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your minNotes account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'notesTaking/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('home'))
