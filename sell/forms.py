from django import forms
from models import ImageAttachment


class SellImageUploadForm(forms.ModelForm):

    class Meta:
        model = ImageAttachment
        fields = ['file']

