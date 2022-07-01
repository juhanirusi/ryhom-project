from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from .models import Article, Comment

# Register your models here.


@admin.action(description='Publish Article(s)')
def publish_article(modeladmin, request, queryset):
    queryset.update(published = True)
    messages.success(request, "Selected Articles(s) Are Now Published!")


@admin.action(description='Unpublish Article(s)')
def unpublish_article(modeladmin, request, queryset):
    queryset.update(published = False)
    messages.success(request, "Selected Article(s) Are Now Unpublished!")


@admin.action(description='Set As Featured')
def set_as_featured(modeladmin, request, queryset):
    queryset.update(featured = True)
    messages.success(request, "Selected Article(s) Are Now Featured!")


@admin.action(description='Remove Featured Status')
def remove_featured_status(modeladmin, request, queryset):
    queryset.update(featured = False)
    messages.success(request, "Selected Article(s) Are Now Removed From Featured!")


class ArticleAdmin(admin.ModelAdmin):
    """Define the article page customization."""
    ordering = ['-modified']
    list_display = ['title', 'author', 'type', 'published', 'likes', 'featured', 'slug']
    list_filter = ('type', 'published', 'featured', 'created', 'modified',)
    search_fields = ['title', 'name', 'username']
    actions = [
        publish_article,
        unpublish_article,
        set_as_featured,
        remove_featured_status
    ]

    fieldsets = (
        (_('Common Info'), {'fields': ('title', 'summary', 'author', 'created', 'modified',)}),
        (_('Featured Image'), {'fields': ('image', 'image_credit',)}),
        (_('Categorizing'), {'fields': ('categories', 'tags', 'type',)}),
        (_('Write The Article'), {'fields': ('content',)}),
        (_('Statuses'), {'fields': ('published', 'featured', 'likes',)}),
        (_('Slug'), {'fields': ('slug',)}),
    )

    readonly_fields = ['created', 'modified']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
