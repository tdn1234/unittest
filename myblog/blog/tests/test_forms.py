from django.test import TestCase, Client

from django.contrib.auth.models import User

from blog.forms import CommentForm, EntryForm

from blog.models import Entry, Comment

import datetime


class EntryFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('abc')
        self.user.email = 'tdn@gmail.com'
        self.entry = Entry.objects.create(author=self.user, title="Test entry")
        self.comment = Comment.objects.create(entry=self.entry, name=self.user.username, email='tdn@gmail.com')

    # def test_init(self):
    #     comment_form = CommentForm()
    #     comment_form.model = Comment

    def test_valid_data(self):
        entry_form = EntryForm({
            'title': self.entry.title,
            'body': 'entry body',
            'author': self.user.id
        })
        self.assertTrue(entry_form.is_valid())

        comment_form = CommentForm({
            'name': 'Test form user',
            'email': 'test@gmail.com',
            'body': 'body content',
            'entry': self.entry.id
        }, instance=self.comment)

        self.assertTrue(comment_form.is_valid())
        comment = comment_form.save()
        self.assertEqual(comment.name, 'Test form user')
        self.assertEqual(comment.email, 'test@gmail.com')
        self.assertEqual(comment.body, 'body content')
        self.assertEqual(comment.entry.id, self.entry.id)


