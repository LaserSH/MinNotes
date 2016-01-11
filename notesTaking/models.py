from django.db import models

class Notebook(models.Model):
    title = models.CharField(max_length=200)
    init_date = models.DateTimeField('date created')
    mod_date = models.DateTimeField('data last modified')
    description = models.CharField(max_length=500)
    def __str__(self):
        return self.title

class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    init_date = models.DateTimeField('date created')
    mod_date = models.DateTimeField('date last modified')
    content = models.TextField()
    def __str__(self):
        return self.title
