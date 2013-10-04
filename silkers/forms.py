from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from models import UserProfile


class RegistrationBasicForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if User.objects.filter(Q(email=email)):
                raise forms.ValidationError(u'This email address is already registered.')

        return email

    def clean_user_name(self):
        username = self.cleaned_data['user_name']
        if username:
            if User.objects.filter(Q(username=username)):
                raise forms.ValidationError(u'This username is already taken.')

        return username

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            msg = u'Passwords do not match. Please try again.'
            self._errors['confirm_password'] = self.error_class([msg])

        return cleaned_data


class RegistrationExtraForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        #TODO: add measurement, picture, and maybe pants size?
        fields = ['shoe_size', 'dress_size', 'city', 'state']
