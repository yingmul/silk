from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.views.generic.edit import FormMixin
from upload.serialize import serialize
from upload.response import JSONResponse, response_mimetype
from sell.models import Picture
from silk.views import LoginRequired
from sell.forms import SellOutfitStepOneForm


class SellOutfitView(LoginRequired, FormMixin, TemplateView):
    template_name = 'sell/picture_form.html'

    def get_context_data(self, **kwargs):
        context = super(SellOutfitView, self).get_context_data(**kwargs)

        context.update({
            'outfit_form': self.outfit_form,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.outfit_form = SellOutfitStepOneForm()
        return super(SellOutfitView, self).get(request, *args, **kwargs)


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

    #TODO: get this to work
    # def get_queryset(self):
    #     return Picture.objects.filter(seller=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
