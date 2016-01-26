import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Note, Notebook

class NoteMethodTests(TestCase):

    def test_dummy(self):
        a = Notebook(title='what', init_date=timezone.now(),
                     mod_date=timezone.now(), description='ww')
        self.assertEqual(a.title, 'what')

class IndexViewTests(TestCase):

    def test_index_view_with_onebook(self):
        response = self.client.get(reverse('notesTaking:index'))
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, '<p>')
        self.assertQuerysetEqual(response.context['notebook_list'], [])
