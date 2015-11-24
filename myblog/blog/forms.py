from django import forms

import datetime

from django.forms import ModelForm

from blog.models import Comment, Entry


# class CommentForm(forms.Form):
#     # email = forms.CharField(widget=forms.TextInput())
#     # name = forms.CharField(label='Name', max_length=120)
#     class Meta:
#         model = Comment
#         fields = ['name', 'email', 'body']


class CommentForm(forms.ModelForm):
    # email = forms.CharField(widget=forms.TextInput())
    # name = forms.CharField(label='Name', max_length=120)
    # entry = forms.CharField(widget=forms.HiddenInput())
    entry = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', 'image')
        # exclude = ['entry']

    # def __init__(self, *args, **kwargs):
    #     self.entry = kwargs.pop('entry')   # the blog entry instance
    #     super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        comment = Comment.objects.create(
            entry_id=data['entry'],
            name=data['name'],
            email=data['email'],
            body=data['body'],
            image=data['image'],
            created_at=datetime.datetime.now()
        )
        comment.save()
        return comment


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ('title', 'body', 'author')
