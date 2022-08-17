from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from ryhom.articles.models import Article
from ryhom.microposts.models import Micropost

from .models import Tag


class ArticlesByTagListView(ListView):
    model = Tag
    context_object_name = 'articles_in_tag'
    template_name = 'tags/articles-by-tag-page.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        queryset = Article.articles.published().by_tag(self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ArticlesByTagListView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class MicropostsByTagListView(ListView):
    model = Tag
    context_object_name = 'microposts_in_tag'
    template_name = 'tags/microposts-by-tag-page.html'
    paginate_by = 2

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        queryset = Micropost.microposts.published().by_tag(tags=self.tag)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MicropostsByTagListView, self).get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
