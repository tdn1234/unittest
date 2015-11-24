from django.shortcuts import render, HttpResponse


from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from blog.models import Entry, Comment
from blog.forms import CommentForm, EntryForm

# Create your views here.


class EntryList(ListView):
    model = Entry
    context_object_name = 'objects'
    template_name = 'blog/entries_list.html'


class EntryDetail(DetailView):
    model = Entry
    context_object_name = 'object'
    template_name = 'blog/entry_detail.html'
    form_class = CommentForm

    # def get_form_kwargs(self):
    #     kwargs = super(EntryDetail, self).get_form_kwargs()
    #     # kwargs['object'] = self.get_object()
    #     return kwargs

    # def get_context_data(self, **kwargs):
    #     d = super(EntryDetail, self).get_context_data(**kwargs)
    #     d['entry'] = self.get_object()
    #     return d

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        # call to base implementation first to get a context
        # context = super(EntryDetail, self).get_context_data(**kwargs)
        # add in the query set of all entry's comments
        context = {}
        context['object'] = Entry.objects.get(pk=self.kwargs['pk'])
        if 'forms' in self.kwargs:
            # return HttpResponse(self.kwargs['forms'])
            context['forms'] = self.kwargs['forms']
        else:
            context['forms'] = CommentForm(initial={'entry': self.kwargs['pk']})

        context['comments'] = Comment.objects.filter(entry_id=self.kwargs['pk'])
        return context

    def post(self, request, pk):
        # return HttpResponse(request.POST['entry_id'])
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Your comment submitted successfully')
        else:
            self.kwargs['forms'] = form
            return self.render_to_response(self.get_context_data(forms=form))


class EntryCreate(FormView):
    template_name = 'blog/entry_create.html'
    form_class = EntryForm

    def get(self, request, *args, **kwargs):
        form_class = self.form_class
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        return HttpResponse('Your entry has been submitted')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# class CommentView(FormView):
#     template_name = 'blog/comment_form.html'
#     form_class = CommentForm
#
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super(CommentView, self).form_valid(form)


