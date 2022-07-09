from django.contrib import admin, messages
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _

from .models import Micropost, MicropostComment

# Register your models here.


@admin.action(description='Publish Post(s)')
def publish_post(modeladmin, request, queryset):
    queryset.update(published=True)
    messages.success(request, "Selected Post(s) Are Now Published!")


@admin.action(description='Unpublish Post(s)')
def unpublish_post(modeladmin, request, queryset):
    queryset.update(published=False)
    messages.success(request, "Selected Post(s) Are Now Unpublished!")


class MicropostAdmin(admin.ModelAdmin):
    """Define the article page customization."""
    ordering = ['-modified']
    list_display = ['title', 'author', 'likes', 'published']
    list_filter = ('author', 'likes', 'published',)
    search_fields = ['title', 'content']
    actions = [publish_post, unpublish_post]
    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    fieldsets = (
        (_('Common Info'), {'fields': ('title', 'author', 'created', 'modified',)}),
        (_('Featured Image'), {'fields': ('image', 'image_credit',)}),
        (_('Post Text'), {'fields': ('content',)}),
        (_('Tags'), {'fields': ('tags',)}),
        (_('Slug'), {'fields': ('slug',)}),
    )

    readonly_fields = ['created', 'modified', 'slug']


admin.site.register(Micropost, MicropostAdmin)
admin.site.register(MicropostComment)
