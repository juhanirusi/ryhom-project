from django.views.generic import ListView
from ryhom.articles.models import Article

from .models import Tag


class TagDetailView(ListView):
    model = Tag
    context_object_name = 'tag'
    template_name = 'tags/tag-page.html'

    def get_queryset(self):
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        self.queryset = Article.objects.filter(tags=tag)
        return tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        context['posts_in_tag'] = self.queryset
        return context
