import os
import uuid
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_protect
from django.contrib.formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.views.generic.edit import FormMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse

from silkers.forms import RegistrationBasicForm, RegistrationExtraForm, LoginForm
from models import UserProfile
from sell.models import Picture

FORMS = [("0", RegistrationBasicForm),
         ("1", RegistrationExtraForm)]

TEMPLATES = {"0": "silkers/registration_basic_form.html",
             "1": "silkers/registration_extra_form.html"}


class RegistrationWizard(SessionWizardView):
    #TODO DEPLOY
    # file_storage = FileSystemStorage(
    #     location=os.path.join(settings.MEDIA_ROOT, 'profile', str(uuid.uuid4())[:8]))

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
        # Now log the user in after registration
        auth_user = authenticate(username=user_data['user_name'], password=user_data['password'])
        if auth_user is not None:
            if auth_user.is_active:
                login(self.request, auth_user)
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
        self.request.session.set_test_cookie()

        self.login_form = LoginForm()
        self.request = request
        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        login(self.request, self.login_form.get_user())
        return super(LoginView, self).form_valid(form)

    @sensitive_post_parameters()
    def post(self, request, *args, **kwargs):
        self.request = request
        #BUG: not quite working, fix this (may need to set test cookie somewhere else instead of get
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            self.login_form = LoginForm(data=request.POST)

            if self.login_form.is_valid():
                return self.form_valid(self.login_form)
            else:
                return self.form_invalid(self.login_form)
        else:
            return HttpResponse("Please enable cookies and try again.")


@sensitive_post_parameters()
@csrf_protect
def logout_view(request):
    # on log out, remove any outfit and piece photos that were not tied to the outfits/pieces
    pics = Picture.objects.filter(
        seller=request.user,
        piece__isnull=True,
        type='p'
    ) | Picture.objects.filter(
        seller=request.user,
        outfit__isnull=True,
        type='o'
    )

    for pic in pics:
        pic.delete()

    logout(request)
    return HttpResponseRedirect(reverse('home'))

