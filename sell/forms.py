from django import forms
from sell.models import Piece

class SellOutfitStepOneForm(forms.Form):
    """
    First step of selling an outfit, including basic info of outfit and its pictures
    """
    name = forms.CharField(max_length=50, label=u'Name of Outfit')
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=u'Description (Optional)'
    )


class SellOutfitStepTwoForm(forms.ModelForm):
    """
    Second step of selling an outfit, including upload pictures of individual pieces to sell
    """
    class Meta:
        model = Piece
        fields = ['price', 'brand', 'category', 'condition']
