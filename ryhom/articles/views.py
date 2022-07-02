from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import CreateView

from .forms import AddArticleForm


class AddArticleView(LoginRequiredMixin, CreateView):
    form_class = AddArticleForm
    template_name = 'articles/add-article.html'
    success_url = reverse_lazy('articles:add_article')

    def get_initial(self):
        author = self.request.user
        return {'author': author,}

    def form_valid(self, form):
        if 'save_for_later' in self.request.POST:
            form.instance.status = 'Saved For Later'
            messages.success(self.request, 'Your article was saved!')
        else: # elif submit_for_review' in self.request.POST:
            form.instance.status = 'Wants To Publish'
            messages.success(self.request,
                'Good job, we\'ll review your article, \
                and notify you once it\'s published!')

        return super().form_valid(form)
