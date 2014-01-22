from django import forms
from models import Comment


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={
                'cols': 59,
                'rows': 2,
                'placeholder': 'Add your comment'
            }
        )
    )

    class Meta:
        model = Comment
        fields = ['comment']
