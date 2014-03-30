import os
import uuid
import urlparse
import json

from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.contrib.auth import REDIRECT_FIELD_NAME, authenticate
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

from silkers.forms import RegistrationBasicForm, RegistrationExtraForm, LoginForm, RegistrationForm, ProfileForm
from models import UserProfile
from sell.models import Picture

FORMS = [("0", RegistrationBasicForm),
         ("1", RegistrationExtraForm)]

TEMPLATES = {"0": "silkers/registration_basic_form.html",
             "1": "silkers/registration_extra_form.html"}

#TODO: not being used, no longer need a wizard, create the userprofile only when user sells
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


class ProfileView(FormMixin, TemplateView):
    template_name = 'silkers/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({
            'profile_form': self.profile_form,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.profile_form = ProfileForm()
        self.request = request

        return super(ProfileView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('sell')

    def form_valid(self, form):
        return super(ProfileView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.profile_form = ProfileForm(data=request.POST)
        if self.profile_form.is_valid():
            return self.form_valid(self.profile_form)
        else:
            return self.form_invalid(self.profile_form)


def ajax_registration(request):
    '''
    View used for registration cases when user is registering via a modal.
    '''
    if request.POST:
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            # create the user, and log the user in
            user = User.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
            )

            # Now log the user in after registration
            auth_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if auth_user is not None:
                if auth_user.is_active:
                    login(request, auth_user)

            if request.is_ajax():
                return HttpResponse('OK')
            else:
                pass
        else:
            if request.is_ajax():
                # Prepare JSON for parsing
                errors_dict = {}
                if form.errors:
                    for field in form.errors:
                        field_error = form.errors[field]
                        # take the error string out of the field errors
                        field_error_str = ''
                        for e in field_error:
                            field_error_str += e + ' '
                        errors_dict[field] = unicode(field_error_str)
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                # render() form with errors (No AJAX)
                pass
    else:
        form = RegistrationForm()

    return render(
        request,
        'modals/registration.html',
        {
            'form': form,
        })


@sensitive_post_parameters()
@csrf_protect
def ajax_login(request):
    """
    A class used for most login cases: where actions are required to have an account:
    e.g. sell, login in header, comment, etc. It's an ajax login since this login screen
    appears in a modal
    """
    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():     # this does the user authentication
            # actually log the user in
            login(request, form.get_user())
            if request.is_ajax():
                return HttpResponse('OK')
            else:
                pass
        else:
            if request.is_ajax():
                # Prepare JSON for parsing
                errors_dict = {}
                if form.errors:
                    for field in form.errors:
                        field_error = form.errors[field]
                        # take the error string out of the field errors
                        field_error_str = ''
                        for e in field_error:
                            field_error_str += e + ' '
                        errors_dict[field] = unicode(field_error_str)
                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                # render() form with errors (No AJAX)
                pass
    else:
        form = LoginForm()

    return render(
        request,
        'modals/login.html',
        {
          'login_form': form,
          REDIRECT_FIELD_NAME: request.REQUEST.get(REDIRECT_FIELD_NAME)
        })

#TODO: this is not being used right now, but may want to use this for some case, may combine this with ajax_login
#not an ajax login, redirect to the login redirect url
class LoginView(FormMixin, TemplateView):
    template_name = 'modals/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context.update({
            'login_form': self.login_form,
            REDIRECT_FIELD_NAME: self.request.REQUEST.get(REDIRECT_FIELD_NAME),
        })
        return context

    def get(self, request, *args, **kwargs):
        self.request.session.set_test_cookie()

        self.login_form = LoginForm()
        self.request = request

        return super(LoginView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        redirect_to = self.request.REQUEST.get(REDIRECT_FIELD_NAME, '')

        netloc = urlparse.urlparse(redirect_to)[1]

         # Use default setting if redirect_to is empty
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

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

