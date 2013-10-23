from django.views.generic import CreateView, ListView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from upload.serialize import serialize
from upload.response import JSONResponse, response_mimetype
from sell.models import Picture, Outfit
from silk.views import LoginRequired
from sell.forms import SellOutfitStepOneForm, SellOutfitStepTwoForm


FORMS = [("0", SellOutfitStepOneForm),
         ("1", SellOutfitStepTwoForm)]

TEMPLATES = {"0": "sell/sell_outfit_1.html",
             "1": "sell/sell_outfit_2.html"}


class SellWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        outfit_form_data = form_list[0].cleaned_data

        outfit = Outfit.objects.create(
            user=self.request.user,
            name=outfit_form_data['name'],
            description=outfit_form_data['description'],
        )

        # set the outfit to all the pictures that were created in this form
        pictures = Picture.objects.filter(
            seller=self.request.user,
            outfit__isnull=True)

        for picture in pictures:
            picture.outfit = outfit
            picture.save()

        return HttpResponseRedirect('/')


class PictureCreateView(LoginRequired, CreateView):
    model = Picture

    def form_valid(self, form):
        # setting seller to be the logged in user
        form.instance.seller = self.request.user
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureDeleteView(LoginRequired, DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(LoginRequired, ListView):
    model = Picture

    # Display only the pictures that were created by this user, and hasn't tied to an outfit yet
    def get_queryset(self):
        return Picture.objects.filter(seller=self.request.user, outfit__isnull=True)

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
