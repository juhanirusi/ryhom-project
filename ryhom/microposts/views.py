from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView

from .forms import AddMicropostCommentForm, AddMicropostForm
from .models import Micropost, MicropostComment

# Create your views here.

class AddMicropostView(LoginRequiredMixin, CreateView):
    form_class = AddMicropostForm
    template_name = 'microposts/add-micropost.html'

    def get_initial(self):
        author = self.request.user
        return {'author': author,}

    def form_valid(self, form):
        form.instance.published = True
        messages.success(self.request,
            'Good job, your new post has been published'
        )

        return super().form_valid(form)

    def get_success_url(self):
        success_url = reverse_lazy(
                'accounts:user_profile',
                args=[self.request.user.slug]
            )

        return success_url


class DeleteMicropostView(LoginRequiredMixin, DeleteView):
    model = Micropost
    template_name = 'microposts/delete-micropost.html'
    success_url = reverse_lazy('accounts:my_posts')
    success_message = 'The micropost has been deleted'

    def get_object(self):
        # Only the rightful author of the article will get to
        # edit it, otherwise show a 404 error.
        return get_object_or_404(
            Micropost.objects.filter(author=self.request.user),
            uuid=self.kwargs['micropost_uuid']
        )

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AllMicropostsListView(ListView):
    model = Micropost
    paginate_by = 2
    template_name = 'microposts/all-microposts.html'
    context_object_name = 'microposts'
    ordering = '-created'
    # With annotate + Count, we can add the number of comments a
    # specific micropost has into the context data.
    queryset = Micropost.objects.filter(published=True).annotate(
        comment_count=Count('micropostcomment')
    )


class MicropostDetailView(DetailView):
    template_name = 'microposts/micropost-detail.html'
    model = Micropost
    queryset = Micropost.objects.filter(published=True)

    # def get_context_data(self, **kwargs):
    #     context = super(ArticleDetailView, self).get_context_data(**kwargs)
    #     context['author'] = Article.objects.filter(slug=self.object.author).first()
    #     context['slug'] = Article.objects.filter(slug=self.object.slug).first()
    #     return context

    def get_object(self):
        self.micropost = get_object_or_404(self.queryset, slug=self.kwargs['micropost_slug'])
        return self.micropost

    def get_context_data(self , **kwargs):
        context = super(MicropostDetailView, self).get_context_data(**kwargs)
        connected_comments = MicropostComment.objects.filter(post=self.micropost)
        number_of_comments = connected_comments.count()

        context['micropost_author'] = self.micropost.author
        context['comments'] = connected_comments
        context['nro_of_comments'] = number_of_comments
        context['comment_form'] = AddMicropostCommentForm()
        return context

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            form = AddMicropostCommentForm(self.request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                try:
                    parent = form.cleaned_data['parent']
                except:
                    parent=None

            new_comment = MicropostComment(
                comment=comment,
                author=self.request.user,
                post=self.get_object(),
                parent=parent
            )

            new_comment.save()
            return redirect(self.request.path_info)


class AddRemoveMicropostLike(LoginRequiredMixin, View):
    def post(self, request, micropost_pk, *args, **kwargs):
        micropost = Micropost.objects.get(pk=micropost_pk)

        is_like = False

        for like in micropost.likers.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            micropost.likers.add(request.user)

        if is_like:
            micropost.likers.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddRemoveMicropostCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = MicropostComment.objects.get(pk=pk)

        is_like = False

        for like in comment.likers.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likers.add(request.user)

        if is_like:
            comment.likers.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
