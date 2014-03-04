import floppyforms as forms
from models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': 2,
                'placeholder': 'Add your comment'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['comment']
