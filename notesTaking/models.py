from django.db import models
from datetime import datetime
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Notebook(models.Model):
    title = models.CharField(max_length=200)
    init_date = models.DateTimeField('date created')
    mod_date = models.DateTimeField('date last modified')
    description = models.CharField(max_length=500)
    slug = models.SlugField(default='Untitled')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.mod_date = datetime.now();
        super(Notebook, self).save(*args, **kwargs);

    def __str__(self):
        return self.title

class Note(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    init_date = models.DateTimeField('date created')
    mod_date = models.DateTimeField('date last modified')
    content = models.TextField()
    slug = models.SlugField(default='Untitled')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.mod_date = datetime.now();
        super(Note, self).save(*args, **kwargs);

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
