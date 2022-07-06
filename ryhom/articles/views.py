from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import AddArticleForm, AddCommentForm
from .models import Article, Comment


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
    queryset = Article.objects.filter(status='Published')

    # def get_context_data(self, **kwargs):
    #     context = super(ArticleDetailView, self).get_context_data(**kwargs)
    #     context['author'] = Article.objects.filter(slug=self.object.author).first()
    #     context['slug'] = Article.objects.filter(slug=self.object.slug).first()
    #     return context

    def get_object(self):
        self.article = get_object_or_404(self.queryset, slug=self.kwargs['article_slug'])
        return self.article

    def get_context_data(self , **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        connected_comments = Comment.objects.filter(article=self.article)
        number_of_comments = connected_comments.count()

        context['article_author'] = self.article.author.slug
        context['comments'] = connected_comments
        context['nro_of_comments'] = number_of_comments
        context['comment_form'] = AddCommentForm()
        return context

    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            form = AddCommentForm(self.request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                try:
                    parent = form.cleaned_data['parent']
                except:
                    parent=None

            new_comment = Comment(
                comment=comment,
                author=self.request.user,
                article=self.get_object(),
                parent=parent
            )

            new_comment.save()
            return redirect(self.request.path_info)


















# class AddCommentLike(LoginRequiredMixin, View):
#     def post(self, request, post_pk, pk, *args, **kwargs):
#         comment = Comment.objects.get(pk=pk)
#         is_dislike = False
#         for dislike in comment.dislikes.all():
#             if dislike == request.user:
#                 is_dislike = True
#                 break
#         if is_dislike:
#             comment.dislikes.remove(request.user)
#         is_like = False
#         for like in comment.likes.all():
#             if like == request.user:
#                 is_like = True
#                 break
#         if not is_like:
#             comment.likes.add(request.user)

#         if is_like:
#             comment.likes.remove(request.user)
#         next = request.POST.get('next', '/')
#         return HttpResponseRedirect(next)
# class AddCommentDislike(LoginRequiredMixin, View):
#     def post(self, request, post_pk, pk, *args, **kwargs):
#         comment = Comment.objects.get(pk=pk)
#         is_like = False
#         for like in comment.likes.all():
#             if like == request.user:
#                 is_like = True
#                 break
#         if is_like:
#             comment.likes.remove(request.user)
#         is_dislike = False
#         for dislike in comment.dislikes.all():
#             if dislike == request.user:
#                 is_dislike = True
#                 break
#         if not is_dislike:
#             comment.dislikes.add(request.user)

#         if is_dislike:
#             comment.dislikes.remove(request.user)
#         next = request.POST.get('next', '/')
#         return HttpResponseRedirect(next)
