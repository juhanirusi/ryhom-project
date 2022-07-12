from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from ryhom.articles.models import Article
from ryhom.microposts.models import Micropost

from .models import Tag


class ArticlesByTagListView(ListView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tags/articles-by-tag-page.html'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        self.queryset = Article.objects.filter(tags=tag)
        return tag

    def get_context_data(self, **kwargs):
        context = super(ArticlesByTagListView, self).get_context_data(**kwargs)
        context['articles_in_tag'] = self.queryset
        return context


class MicropostsByTagListView(ListView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tags/microposts-by-tag-page.html'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        self.queryset = Micropost.objects.filter(tags=tag)
        return tag

    def get_context_data(self, **kwargs):
        context = super(MicropostsByTagListView, self).get_context_data(**kwargs)
        context['microposts_in_tag'] = self.queryset
        return context
