from django.forms import ModelForm
from django.forms.widgets import HiddenInput, TextInput

from .models import Micropost, MicropostComment


class AddMicropostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddMicropostForm, self).__init__(*args, **kwargs)
        self.fields['author'].disabled = True
        self.fields['author'].widget = HiddenInput()

        self.fields['title'].widget.attrs[
            'placeholder'
        ] = 'Give your post a title'

        #self.fields['title'].widget.attrs.update({'class': 'special'})
        #self.fields['title'].widget.attrs.update(size='100')

        self.fields['image_credit'].widget.attrs[
            'placeholder'
        ] = 'Enter the owner of the image'

        self.fields['content'].widget.attrs[
            'placeholder'
        ] = 'Enter some content to descripe what\'s happening in the image...'

    class Meta:
        model = Micropost
        fields = (
            'author', 'title', 'image', 'image_credit', 'content'
        )
        labels = {
            'author': '',
            'title': 'Post Title',
            'image': 'Image',
            'image_credit': 'Image Credit (optional)',
            'content': 'Content',
        }
        help_texts = {
            'image_credit': 'Who owns or created this image?',
        }


class AddMicropostCommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddMicropostCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['placeholder'] = 'Add your comment...'

    class Meta:
        model = MicropostComment
        fields = ('comment', 'parent')
        labels = {
            'comment': '',
        }

        widgets = {
            'content' : TextInput(),
        }
