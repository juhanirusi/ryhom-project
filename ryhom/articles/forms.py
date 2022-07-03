from django.forms import ModelForm
from django.forms.widgets import HiddenInput

from .models import Article


class AddArticleForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddArticleForm, self).__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['author'].widget = HiddenInput()

        self.fields['title'].widget.attrs['placeholder'] = 'Give your article a title'
        #self.fields['title'].widget.attrs.update({'class': 'special'})
        #self.fields['title'].widget.attrs.update(size='100')

        self.fields['image_credit'].widget.attrs['placeholder'] = 'Enter the owner of the image'

        self.fields['summary'].widget.attrs['placeholder'] = 'Enter a summary'

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
