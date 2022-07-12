from django.forms import ModelForm
from django.forms.widgets import HiddenInput, TextInput

from .models import Article, ArticleComment


class AddEditArticleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddEditArticleForm, self).__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['author'].widget = HiddenInput()

        self.fields['title'].widget.attrs[
            'placeholder'] = 'Give your article a title'
        #self.fields['title'].widget.attrs.update({'class': 'special'})
        #self.fields['title'].widget.attrs.update(size='100')

        self.fields['image_credit'].widget.attrs[
            'placeholder'] = 'Enter the owner of the image'

        self.fields['summary'].widget.attrs[
            'placeholder'
        ] = 'Enter a summary of the contents of the article...'

    class Meta:
        model = Article
        fields = (
            'author', 'title', 'summary', 'image', 'image_credit', 'content'
        )
        labels = {
            'author': '',
            'title': 'Article Title',
            'image': 'Thumbnail Image',
            'image_credit': 'Image Credit (optional)',
            'summary': 'Article Summary',
        }
        help_texts = {
            'image_credit': 'Who owns or created this image?',
            'summary': 'Add a brief summary about the content of the article',
        }


class AddArticleCommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddArticleCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['placeholder'] = 'Add your comment...'

    class Meta:
        model = ArticleComment
        fields = ('comment', 'parent')
        labels = {
            'comment': '',
        }

        widgets = {
            'content' : TextInput(),
        }
