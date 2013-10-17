from django.views.generic.base import TemplateView
from django.views.generic.edit import FormMixin
from forms import SellImageUploadForm

class SellOutfitView(FormMixin, TemplateView):
    template_name = 'sell/outfit_post.html'

    def get_context_data(self, **kwargs):
        context = super(SellOutfitView, self).get_context_data(**kwargs)

        context.update({
            'sell_form': self.sell_form,
        })
        return context

    def get(self, request, *args, **kwargs):
        self.sell_form = SellImageUploadForm()
        self.request = request

        return super(SellOutfitView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.request = request
        self.sell_form = SellImageUploadForm(data=request.POST, prefix='sell')
