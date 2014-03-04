import floppyforms as forms
from django.utils.translation import ugettext_lazy as _
from sell.models import Piece, Picture


make_primary_error_message=\
    _(u"Please select a primary photo from above by clicking on the 'Make Primary' button. "
      u"This photo will be made the display photo.")

class SellOutfitForm(forms.Form):
    """
    First step of selling an outfit, including basic info of outfit and its pictures
    """
    name = forms.CharField(
        max_length=50,
        label=u'Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u"Give your outfit a cool name.")
            }
        ),
    )

    price = forms.DecimalField(
        required=False,
        widget = forms.TextInput(
            attrs={
                'placeholder': _(u"Price for all the pieces for sale in this outfit.")
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'placeholder':
                _(u"What inspired you? Where or when would you wear this outfit? Share your story!")
            }
        ),
        max_length=500,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellOutfitForm')
        super(SellOutfitForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        outfit_pics = Picture.objects.filter(
            seller=self.request.user,
            type='o',
            outfit__isnull=True)

        if not outfit_pics:
            raise forms.ValidationError(u'Remember to upload one or more of your outfit photos!')

        # make sure primary photo was selected
        if outfit_pics.filter(is_primary=True).count() == 0:
            if outfit_pics.count() == 1:
                # if there is only one outfit picture, default this to primary
                for pic in outfit_pics:
                    pic.is_primary=True
                    pic.save()
            else:
                raise forms.ValidationError(make_primary_error_message)
        return self.cleaned_data


class SellPieceForm(forms.ModelForm):
    """
    Second step of selling an outfit, including upload pictures of individual pieces to sell
    """
    #TODO: fix this so we don't need to do these one off definitons. Can use monkey patching to fix
    # This is needed for now to use HTML5 form to do client side validation
    price = forms.DecimalField(
        required=True
    )

    size = forms.CharField(
        required=True,
        widget = forms.TextInput(
            attrs={
                'placeholder': _(u"Enter 'N/A' if there is no size.")
            }
        )
    )

    brand = forms.CharField(
        required=True
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': 5,
                'placeholder':
                _(u"Any damages? Does the size run too small or too large?")
            }
        ),
        max_length=500,
        required=False,
    )

    CHOICES = ((1, 'Yes',), (0, 'No',))
    more_pieces = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=CHOICES,
        required=True,
        label=_(u"Are there more pieces from this outfit you'd like to sell?")
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
             self.request = kwargs['request']
             del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellPieceForm')
        super(SellPieceForm, self).__init__(*args, **kwargs)

    def clean(self):
        # need to make sure the seller uploaded pictures in the fileupload form
        if self.request.session['check_for_sell_piece_pics']:
            # set this value back to False, so calls from FormWizards will not need to check again
            # for this instance of the form
            self.request.session['check_for_sell_piece_pics'] = False

            # use self.prefix as current step, minor hack :)
            piece_pics = Picture.objects.filter(
                seller=self.request.user,
                type='p',
                piece__isnull=True,
                piece_step=int(self.prefix))

            if not piece_pics:
                # throw an error to tell seller to upload pictures for outfit
                raise forms.ValidationError(_(u'Remember to upload one or more photos above!'))

            # make sure primary photo was selected
            if piece_pics.filter(is_primary=True).count() == 0:
                if piece_pics.count() == 1:
                    # if there is only one photo, just mark this as primary
                    for pic in piece_pics:
                        pic.is_primary = True
                        pic.save()
                else:
                    raise forms.ValidationError(make_primary_error_message)
        return self.cleaned_data

    class Meta:
        model = Piece
        fields = ['price', 'size', 'brand', 'category', 'condition', 'description']


class SellPreviewForm(forms.Form):
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            raise Exception('Request was not passed in kwargs when initializing form SellPieceForm')
        super(SellPreviewForm, self).__init__(*args, **kwargs)
