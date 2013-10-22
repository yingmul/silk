from django import forms


class SellOutfitStepOneForm(forms.Form):
    """
    First step of selling an outfit, including basic info of outfit and its pictures
    """
    name = forms.CharField(max_length=50)
    description = forms.CharField(widget=forms.Textarea)

