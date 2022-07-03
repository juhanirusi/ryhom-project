from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import AddArticleForm
from .models import Article


class AddArticleView(LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'articles/add-article.html'

    def get_initial(self):
        author = self.request.user
        return {'author': author,}

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
            success_url = reverse_lazy(
                'accounts:user_profile',
                args=[self.request.user.slug]
            )

        return success_url


class UserPostsView(LoginRequiredMixin, ListView):
    template_name = 'articles/user-posts.html'
    context_object_name = 'published_articles'
    model = Article

    def get_context_data(self, **kwargs):
        # REMEMBER TO ADD MICROPOSTS AS EXTRA CONTEXT AS WELL!
        context = super(UserPostsView, self).get_context_data(**kwargs)
        context.update({
            'saved_articles': Article.user_posts.draft_articles(self.request.user),
            'waiting_review_articles': Article.user_posts.waiting_review_articles(self.request.user),
            #'even_more_context': Model.objects.all(),
        })
        return context

    def get_queryset(self):
        return Article.user_posts.published_articles(self.request.user)


class ArticleDetailView(DetailView):
    template_name = 'articles/article-detail.html'
    model = Article
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'
    # query_pk_and_slug = True
    queryset = Article.objects.filter(status='Published')

    # def get_context_data(self, **kwargs):
    #     context = super(ArticleDetailView, self).get_context_data(**kwargs)
    #     context['author'] = Article.objects.filter(slug=self.object.author).first()
    #     context['slug'] = Article.objects.filter(slug=self.object.slug).first()
    #     return context

    def get_object(self):
        return get_object_or_404(self.queryset,
            author__slug=self.kwargs['author'],
            slug=self.kwargs['slug']
        )
