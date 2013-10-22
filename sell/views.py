from django.views.generic import CreateView, ListView, DeleteView
from upload.serialize import serialize
from sell.models import Picture
from upload.response import JSONResponse, response_mimetype
from silk.views import LoginRequired

# class SellOutfitView(LoginRequired, FormMixin, TemplateView):
#     template_name = 'sell/outfit_post.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(SellOutfitView, self).get_context_data(**kwargs)
#
#         context.update({
#             'sell_form': self.sell_form,
#         })
#         return context
#
#     def get(self, request, *args, **kwargs):
#         self.sell_form = SellImageUploadForm()
#         self.request = request
#
#         return super(SellOutfitView, self).get(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         self.request = request
#         self.sell_form = SellImageUploadForm(data=request.POST, prefix='sell')


class PictureCreateView(LoginRequired, CreateView):
    model = Picture

    def form_valid(self, form):
        # setting creator to be the logged in user
        form.instance.creator = self.request.user
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

    def get_queryset(self):
        return Picture.objects.filter(creator=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
