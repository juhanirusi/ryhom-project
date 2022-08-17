from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import AddArticleCommentForm, AddEditArticleForm
from .models import Article, ArticleComment


class AddArticleView(LoginRequiredMixin, CreateView):
    form_class = AddEditArticleForm
    template_name = 'articles/add-article.html'

    def get_initial(self):
        author = self.request.user
        return {'author': author}

    def form_valid(self, form):
        if 'save_for_later' in self.request.POST:
            form.instance.status = 'Saved For Later'
            messages.success(self.request, 'Your article was saved!')
        else: #'submit_for_review' in self.request.POST:
            form.instance.status = 'Wants To Publish'
            messages.success(self.request,
                'Good job, we\'ll review your article, \
                and notify you once it\'s published!')

        return super().form_valid(form)

    def get_success_url(self):
        if 'save_for_later' in self.request.POST:
            success_url = reverse_lazy('articles:add_article')
        else: #'submit_for_review' in self.request.POST:
            success_url = reverse_lazy('accounts:my_posts')

        return success_url


class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'articles/edit-article.html'
    form_class = AddEditArticleForm

    def get_object(self):
        # Only the rightful author of the article will get to
        # edit it, otherwise show a 404 error.
        return get_object_or_404(
            Article.objects.filter(author=self.request.user),
            uuid=self.kwargs['article_uuid']
        )

    def form_valid(self, form):
        if 'save_for_later' in self.request.POST:
            form.instance.status = 'Saved For Later'
            messages.success(self.request, 'Your article was saved!')
        else: #'submit_for_review' in self.request.POST:
            form.instance.status = 'Wants To Publish'
            messages.success(self.request,
                'Good job, we\'ll review your article, \
                and notify you once it\'s published!')

        return super().form_valid(form)

    def get_success_url(self):
        if 'save_for_later' in self.request.POST:
            success_url = reverse_lazy('articles:edit_article', args=[self.object.uuid])
        else: #'submit_for_review' in self.request.POST:
            success_url = reverse_lazy('accounts:my_posts')

        return success_url


class DeleteArticleView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'articles/delete-article.html'
    success_url = reverse_lazy('accounts:my_posts')
    success_message = 'The article has been deleted'

    def get_object(self):
        # Only the rightful author of the article will get to
        # edit it, otherwise show a 404 error.
        return get_object_or_404(
            Article.objects.filter(author=self.request.user),
            uuid=self.kwargs['article_uuid']
        )

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class ArticleDetailView(DetailView):
    template_name = 'articles/article-detail.html'
    model = Article
    queryset = Article.articles.published()

    def get_object(self):
        self.article = get_object_or_404(self.queryset, slug=self.kwargs['article_slug'])
        return self.article

    def get_context_data(self , **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        connected_comments = ArticleComment.objects.filter(article=self.article)
        number_of_comments = connected_comments.count()

        context['article_author'] = self.article.author
        context['comments'] = connected_comments
        context['nro_of_comments'] = number_of_comments
        context['comment_form'] = AddArticleCommentForm()
        return context

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            form = AddArticleCommentForm(self.request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                try:
                    parent = form.cleaned_data['parent']
                except:
                    parent=None

            new_comment = ArticleComment(
                comment=comment,
                author=self.request.user,
                article=self.get_object(),
                parent=parent
            )

            new_comment.save()
            return redirect(self.request.path_info)


class AddRemoveArticleCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = ArticleComment.objects.get(pk=pk)

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
