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
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellOutfitStepOneForm')
        super(SellOutfitForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        outfit_pics = Picture.objects.filter(
            seller=self.request.user,
            type='o',
            outfit__isnull=True)

        if not outfit_pics:
            raise forms.ValidationError(u'Remember to upload one or more of your outfit pictures!')

        # make sure primary photo was selected
        if outfit_pics.filter(is_primary=True).count() == 0:
            if outfit_pics.count() == 1:
                # if there is only one outfit picture, default this to primary
                for pic in outfit_pics:
                    pic.is_primary=True
                    pic.save()
            else:
                raise forms.ValidationError(u'Please select one of the pictures as the default display picture.')
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
        if 'request' in kwargs:
             self.request = kwargs['request']
             del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellOutfitStepTwoForm')
        super(SellPieceForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        if self.request.session['check_for_sell_piece_pics']:
            # set this value back to False, so calls from FormWizards will not need to check again
            # for this instance of the form
            self.request.session['check_for_sell_piece_pics'] = False

            piece_pics = Picture.objects.filter(
                seller=self.request.user,
                type='p',
                piece__isnull=True,
                piece_step=0)

            if not piece_pics:
                # throw an error to tell seller to upload pictures for outfit
                raise forms.ValidationError(u'Remember to upload one or more pictures!')

            # make sure primary photo was selected
            if piece_pics.filter(is_primary=True).count() == 0:
                if piece_pics.count() == 1:
                    # if there is only one photo, just mark this as primary
                    for pic in piece_pics:
                        pic.is_primary = True
                        pic.save()
                else:
                    raise forms.ValidationError(u'Please select one of the pictures as the primary picture.')
        return self.cleaned_data

    class Meta:
        model = Piece
        fields = ['price', 'brand', 'category', 'condition']


class SellPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellPieceForm')
        super(SellPreviewForm, self).__init__(*args, **kwargs)
