from django.test import TestCase

from django_webtest import WebTest

from blog.models import Entry, Comment

from blog.forms import EntryForm, CommentForm

from django.contrib.auth.models import User

from webtest import Upload


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class EntryViewTest(WebTest):

    def setUp(self):
        self.user = User.objects.create_user('tdn')
        self.entry = Entry.objects.create(author=self.user, title="Test Entry")
        self.comment = Comment.objects.create(entry=self.entry, )
        self.email_error = 'email'
        self.name_error = 'name'
        self.body_error = 'body'

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        self.assertEqual(len(page.forms), 1)

    def test_from_submission_error(self):
        page = self.app.get(self.entry.get_absolute_url())
        page = page.form.submit()
        self.assertContains(page, 'Errors')
        page.form['name'] = 'tdn12'
        page = page.form.submit()
        self.assertEqual(self.email_error, page.pyquery('.form-errors-email').text())
        self.assertEqual(self.body_error, page.pyquery('.form-errors-body').text())
        # test form submission successful
        page.form['email'] = 'tdn@gmail.com'
        page.form['body'] = 'body content'
        page = page.form.submit()
        self.assertContains(page, 'successful')

    def test_entry_form_submission(self):
        page = self.app.get('/blog/entry/create/')
        # assert entry creation form display
        self.assertEqual(len(page.forms), 1)
        response = page.forms[0].submit()
        # user will see warning when they do not fill all required fields before submitting
        self.assertContains(response, 'This field is required')
        page.forms[0]['title'] = 'test entry'
        page.forms[0]['body'] = 'this is body'
        page.forms[0]['author'].select(text='tdn')
        response = page.forms[0].submit()
        # assert case when user submit their entry successfully
        self.assertContains(response, 'Your entry has been submitted')
        # get entry which has been saved, want to make sure we entry has been saved after submitting successfully
        test_entry = Entry.objects.get(pk=2)
        self.assertEqual(test_entry.title, 'test entry')

    def test_upload_image_entry_form(self):
        # check default image accessible
        default_image_path = 'static/images/default.jpg'
        default_image_response = self.app.get('/' + str(default_image_path))
        self.assertEqual(default_image_response.status_code, 200)

        page = self.app.get(self.entry.get_absolute_url())
        # page.forms[0]['image'] = Upload('test.jpeg')
        page.forms[0]['name'] = 'test without image'
        page.forms[0]['email'] = 'test@gmail.com'
        page.forms[0]['body'] = 'body content'
        page.forms[0].submit()
        comment1 = Comment.objects.get(name="test without image")
        # make sure comment image will be get default image when image is not being uploaded
        self.assertEqual(default_image_path, comment1.image)
        # upload image when submitting comment
        page = self.app.get(self.entry.get_absolute_url())
        page.forms[0]['image'] = Upload('test.jpeg')
        page.forms[0]['name'] = 'test image'
        page.forms[0]['email'] = 'test@gmail.com'
        page.forms[0]['body'] = 'body content'
        page.forms[0]['image'] = Upload('test.jpeg')
        page.forms[0].submit(upload_files=[('test-image', 'test.jpeg')])
        comment2 = Comment.objects.get(name='test image')
        self.assertNotEqual(default_image_path, comment2.image)
        # check if comment being assigned
        #  to related entry
        self.assertEqual(comment2.entry.id, self.entry.id)
        # check is uploaded image being accessible
        comment_image_response = self.app.get('/' + str(comment2.image))
        self.assertEqual(comment_image_response.status_code, 200)

    def test_gravatar_url(self):
        com








