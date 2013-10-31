from django import forms
from sell.models import Piece, Picture


class SellOutfitForm(forms.Form):
    """
    First step of selling an outfit, including basic info of outfit and its pictures
    """
    name = forms.CharField(max_length=50, label=u'Name of Outfit')
    description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label=u'Description (Optional)'
    )

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self._user = kwargs['user']
            del kwargs['user']
        else:
            raise Exception('User was not passed in kwargs when initializing form SellOutfitStepOneForm')
        super(SellOutfitForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        outfit_pics = Picture.objects.filter(
            seller=self._user,
            type='o',
            outfit__isnull=True)

        if not outfit_pics:
            # throw an error to tell seller to upload pictures for outfit
            raise forms.ValidationError(u'Remember to upload one or more of your outfit pictures!')
        return self.cleaned_data


class SellPieceForm(forms.ModelForm):
    """
    Second step of selling an outfit, including upload pictures of individual pieces to sell
    """
    CHOICES = ((1, 'Yes',), (0, 'No',))
    more_pieces = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=True,
        label="Is there any more pieces from this outfit you'd like to sell")

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self._user = kwargs['user']
            del kwargs['user']
        else:
            raise Exception('User was not passed in kwargs when initializing form SellOutfitStepTwoForm')
        super(SellPieceForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        piece_pics = Picture.objects.filter(
            seller=self._user,
            type='p',
            piece__isnull=True)

        if not piece_pics:
            # throw an error to tell seller to upload pictures for outfit
            raise forms.ValidationError(u'Remember to upload one or more pictures!')
        return self.cleaned_data

    class Meta:
        model = Piece
        fields = ['price', 'brand', 'category', 'condition']


class SellPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self._user = kwargs['user']
            del kwargs['user']
        else:
            raise Exception('User was not passed in kwargs when initializing form SellPieceForm')
        super(SellPreviewForm, self).__init__(*args, **kwargs)
