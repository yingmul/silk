from django import forms


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


class SellOutfitStepTwoForm(forms.Form):
    """
    Second step of selling an outfit, including upload pictures of individual pieces to sell
    """
    price = forms.DecimalField(decimal_places=2)
    brand = forms.CharField(max_length=100)
