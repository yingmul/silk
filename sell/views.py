from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.views.generic.edit import FormMixin
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

# class SellOutfitView(LoginRequired, FormMixin, TemplateView):
#     template_name = 'sell/sell_outfit.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(SellOutfitView, self).get_context_data(**kwargs)
#
#         context.update({
#             'outfit_form': self.outfit_form,
#         })
#         return context
#
#     def get(self, request, *args, **kwargs):
#         self.outfit_form = SellOutfitStepOneForm()
#         return super(SellOutfitView, self).get(request, *args, **kwargs)
#
#     # TODO: this is temp only
#     def get_success_url(self):
#         return '.'
#
#     def form_valid(self, form):
#         outfit = Outfit.objects.create(
#             user=self.request.user,
#             name=form.cleaned_data['name'],
#             description=form.cleaned_data['description'],
#         )
#
#         # set the outfit to all the pictures that were created in this form
#         pictures = Picture.objects.filter(
#             seller=self.request.user,
#             outfit__isnull=True)
#
#         for picture in pictures:
#             picture.outfit = outfit
#             picture.save()
#
#         return super(SellOutfitView, self).form_valid(form)
#
#     def post(self, request, *args, **kwargs):
#         self.request = request
#         self.outfit_form = SellOutfitStepOneForm(data=request.POST)
#
#         if self.outfit_form.is_valid():
#             return self.form_valid(self.outfit_form)
#         else:
#             return self.form_invalid(self.outfit_form)


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
