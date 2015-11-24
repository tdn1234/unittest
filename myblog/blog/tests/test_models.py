from django.test import TestCase

from blog.models import Entry, Comment


class EntryModelTest(TestCase):
    def test_string_presentation(self):
        entry = Entry(title="Entry test1")
        self.assertEqual(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Entry._meta.verbose_name_plural), "Entries")

    def test_comment_string(self):
        comment = Comment(body="Anonymoust comment")
        self.assertEqual(str(comment), 'Anonymoust comment')



