from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from ryhom.articles.models import Article

from .models import Category


class CategoryDetailView(ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'categories/category-page.html'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        self.queryset = Article.objects.filter(categories=category)
        return category

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['posts_in_category'] = self.queryset
        return context
