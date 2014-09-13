import floppyforms as forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.translation import ugettext_lazy as _

from models import UserProfile


class RegistrationForm(forms.Form):
    #this has to be under a different name due to the fact that register form popup may
    #appear after user login modal, and if that happens, 'div_id_fieldname' would only pick up the
    #username field from login pop so login.js applyFormFieldError wouldn't work for username
    username_register = forms.CharField(max_length=50, label=u'Username')
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(max_length=30, widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data['email']
        if email:
            if User.objects.filter(Q(email=email)):
                raise forms.ValidationError(u'This email address is already registered.')

        return email

    def clean_username_register(self):
        username = self.cleaned_data['username_register']
        if username:
            if User.objects.filter(Q(username=username)):
                raise forms.ValidationError(u'This username is already taken.')

        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            msg = u'Passwords do not match. Please try again.'
            self._errors['confirm_password'] = self.error_class([msg])

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    """
    The form that contains full user information, prompted during sell or in My Account page
    """
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)

    def save(self, *args, **kw):
        user = kw.get('user')

        profile = super(ProfileForm, self).save(commit=False)
        profile.user = user
        profile.save()

    class Meta:
        model = UserProfile
        #TODO: add measurement, picture, and maybe pants size?
        fields = ['shoe_size', 'dress_size', 'city', 'state']


#TODO: change basic and extra form, so only asked if user wants to sell something,
#and ask only the info that RegistrationForm didn't.
class RegistrationBasicForm(forms.Form):
    """
    First step of the Registration form, requiring User's basic info
    """
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
    """
    Second step of the registration form, asking for extra info like measurement
    """
    class Meta:
        model = UserProfile
        #TODO: add measurement, picture, and maybe pants size?
        fields = ['shoe_size', 'dress_size', 'city', 'state']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(
        max_length=30,
        widget=forms.PasswordInput()
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self.user = None

        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(_(u'The username and/or password is incorrect, please try again.'))
            elif not self.user.is_active:
                raise forms.ValidationError(_(u'This user is inactive.'))
        return self.cleaned_data

    def get_user(self):
        return self.user
