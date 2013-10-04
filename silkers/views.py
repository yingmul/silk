from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from silkers.forms import RegistrationBasicForm, RegistrationExtraForm
from models import UserProfile
from django.contrib.auth.models import User

FORMS = [("0", RegistrationBasicForm),
         ("1", RegistrationExtraForm)]

TEMPLATES = {"0": "silkers/registration_basic_form.html",
             "1": "silkers/registration_extra_form.html"}


class RegistrationWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # create an User and UserProfile
        user_data = form_list[0].cleaned_data
        user = User.objects.create_user(
            username=user_data['user_name'],
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        user_profile_data = form_list[1].cleaned_data
        UserProfile.objects.create(
            user=user,
            shoe_size=user_profile_data['shoe_size'],
            dress_size=user_profile_data['dress_size'],
            city=user_profile_data['city'],
            state=user_profile_data['state']
        )
        return HttpResponseRedirect('/')