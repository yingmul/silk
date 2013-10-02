from django import forms


class RegistrationBasicForm(forms.Form):
    user_name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    password_repeat = forms.CharField(max_length=30, widget=forms.PasswordInput())


class RegistrationExtraForm(forms.Form):
    shoe_size = forms.IntegerField(required=False)
    dress_size = forms.IntegerField(required=False)
    city = forms.CharField(max_length=50, required=False)
    #TODO: add state, measurement, picture, and maybe pants size?
