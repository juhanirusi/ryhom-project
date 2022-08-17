from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from ryhom.articles.models import Article

from .models import Category


class CategoryDetailView(ListView):
    model = Category
    context_object_name = 'articles_in_category'
    template_name = 'categories/category-page.html'
    paginate_by = 2

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        queryset = Article.articles.published().by_category(self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context
