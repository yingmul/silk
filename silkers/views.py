from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from django.contrib.auth import login

from silkers.forms import RegistrationBasicForm, RegistrationExtraForm, LoginForm
from models import UserProfile


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


class LoginView(FormMixin, TemplateView):
    template_name = 'silkers/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        context.update({
            'login_form': self.login_form,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.login_form = LoginForm()

        self.request = request
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, self.login_form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    @sensitive_post_parameters()
    def post(self, request, *args, **kwargs):
        self.request = request
        self.login_form = LoginForm(data=request.POST)

        if self.login_form.is_valid():
            return self.form_valid(self.login_form)
        else:
            return self.form_invalid(self.login_form)
