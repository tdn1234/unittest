from django.test import TestCase
from django.template import Template, Context
from django.contrib.auth.models import User

from blog.models import Entry


class EntryHistoryTagTest(TestCase):
    Template = Template("{% load blog_tags %} {% entry_history %}")

    def setUp(self):
        self.user = User.objects.create(username='tdn')

    def test_blog_show_ups(self):
        entry = Entry.objects.create(author=self.user, title='show ups on history block')
        entry1 = Entry.objects.create(author=self.user, title='Entry 2')
        rendered = self.Template.render(Context({}))
        self.assertIn(entry.title, rendered)
        self.assertNotIn(entry1.title, rendered)

    def test_blog_without_entry(self):
        # Template = Template("{% load blog_tags %}{% entry_history %}")
        rendered = self.Template.render(Context({}))
        self.assertIn('No recent entries', rendered)

