from django import forms
from .models import Note, Notebook

class NotebookForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the category name.")
    description = forms.CharField(max_length=2000, help_text="Please enter the description of the nootbook")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Notebook
        fields = ('title','description')
        exclude = ('notebook','init_date','mod_date')


class NoteForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the Note.")
    content = forms.CharField(widget = forms.Textarea, help_text="Enter your note here")

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Note

        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        # we can either exclude the category field from the form,
        exclude = ('notebook','init_date','mod_date', 'slug')
        #or specify the fields to include (i.e. not include the category field)
        #fields = ('title', 'url', 'views')
