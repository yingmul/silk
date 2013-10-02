from django.contrib.formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from silkers.forms import RegistrationBasicForm, RegistrationExtraForm

FORMS = [("0", RegistrationBasicForm),
         ("1", RegistrationExtraForm)]

TEMPLATES = {"0": "silkers/registration_form.html",
             "1": "silkers/registration_form.html"}


class RegistrationWizard(SessionWizardView):
    def get_template_names(self):
        print self.steps.current
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        # do_something_with_the_form_data(form_list)
        return HttpResponseRedirect('/page-to-redirect-to-when-done/')