from django.views.generic import CreateView, ListView, DeleteView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from upload.serialize import serialize
from upload.response import JSONResponse, response_mimetype
from sell.models import Picture, Outfit, Piece
from silk.views import LoginRequired
from sell.forms import SellOutfitForm, SellPieceForm, SellPreviewForm


FORMS = [("0", SellOutfitForm)]
for i in range(1, settings.MAX_PIECE_SELL_FORMS + 1):
    FORMS.append((str(i), SellPieceForm))

FORMS.append((str(settings.MAX_PIECE_SELL_FORMS+1), SellPreviewForm))

TEMPLATES = {"0": "sell/sell_outfit_1.html"}
for i in range(1, settings.MAX_PIECE_SELL_FORMS + 1):
    TEMPLATES[str(i)]="sell/sell_outfit_2.html"
TEMPLATES[str(settings.MAX_PIECE_SELL_FORMS+1)]="sell/sell_outfit_preview.html"


def show_more_piece_form_condition(wizard):
    """
    Checks if the current step, the user selected 'more_pieces' to No, if true, then skip the next step
    """

    current_step = wizard.storage.current_step
    cleaned_data = wizard.get_cleaned_data_for_step(str(current_step)) or {}
    if cleaned_data:
        more_pieces = cleaned_data.get('more_pieces', None)
        if more_pieces and more_pieces == u'0':
                return False
    return True


class SellWizard(SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_next_step(self, step=None):
        """
        Returns the next step after the given `step`. If no more steps are
        available, None will be returned. If the `step` argument is None, the
        current step will be determined automatically.

        Overrides the behavior, if step is skipped, automatically return the last step
        """
        if step is None:
            step = self.steps.current
        form_list = self.get_form_list()
        try:
            key = form_list.keyOrder.index(step) + 1
        except ValueError:
            # the step with 'key' is skipped, need to move on to the last step
            return form_list.keyOrder[len(form_list.keyOrder)-1]

        if len(form_list.keyOrder) > key:
            return form_list.keyOrder[key]
        return None

    def render_done(self, form, **kwargs):
        """
        This method gets called when all forms passed. The method should also
        re-validate all steps to prevent manipulation. If any form don't
        validate, `render_revalidation_failure` should get called.
        If everything is fine call `done`.

        Overrides check if form data for each form exists, if it doesn't, that means this form
        was skipped, so no need to validate, see below for security concern.
        """
        final_form_list = []
        # walk through the form list and try to validate the data again.
        for form_key in self.get_form_list():
            #aliu: added to check if form_data exists, if none, that means the step was skipped
            #there is a potential security concern where the data was manipulated to be None,
            #since this is not meant to be a secure form, this is a minor concern
            form_data=self.storage.get_step_data(form_key)
            if form_data:
                form_obj = self.get_form(step=form_key,
                    data=form_data,
                    files=self.storage.get_step_files(form_key))
                if not form_obj.is_valid():
                    return self.render_revalidation_failure(form_key, form_obj, **kwargs)
                final_form_list.append(form_obj)

        # render the done view and reset the wizard before returning the
        # response. This is needed to prevent from rendering done with the
        # same data twice.
        done_response = self.done(final_form_list, **kwargs)
        self.storage.reset()
        return done_response

    def get_form_kwargs(self, step):
        """
        Override get_form_kwargs, to pass the user to the form's __init__ via kwargs
        """
        return {'user': self.request.user}

    def process_step(self, form):
        # make sure for the Piece forms, it always shows the pictures of the current piece
        if isinstance(form, SellPieceForm):
            piece_pictures = Picture.objects.filter(
                seller=self.request.user,
                piece__isnull=True,
                type='p',
            )
            for pic in piece_pictures:
                pic.display = False
                pic.save()

            # piece_form_data = form.cleaned_data
            # piece = Piece.objects.create(
            #     price=piece_form_data['price'],
            #     brand=piece_form_data['brand'],
            #     category=piece_form_data['category'],
            #     condition=piece_form_data['condition'],
            # )
            #
            # piece_pictures = Picture.objects.filter(
            #     seller=self.request.user,
            #     piece__isnull=True,
            #     type='p',
            # )
            # for pic in piece_pictures:
            #     pic.piece = piece
            #     pic.save()

        return super(SellWizard, self).process_step(form)

    def done(self, form_list, **kwargs):
        outfit_form_data = form_list[0].cleaned_data

        outfit = Outfit.objects.create(
            user=self.request.user,
            name=outfit_form_data['name'],
            description=outfit_form_data['description'],
        )

        # set the outfit to all the outfit pictures that were created in this form
        outfit_pictures = Picture.objects.filter(
            seller=self.request.user,
            outfit__isnull=True,
            type='o')

        for picture in outfit_pictures:
            picture.outfit = outfit
            picture.save()

        # create piece and set pictures.piece to aht
        piece_form_data = form_list[1].cleaned_data
        piece = Piece.objects.create(
            price=piece_form_data['price'],
            brand=piece_form_data['brand'],
            category=piece_form_data['category'],
            condition=piece_form_data['condition'],
            outfit=outfit,
        )

        piece_pictures = Picture.objects.filter(
            seller=self.request.user,
            piece__isnull=True,
            type='p'
        )
        # set all the piece picture's piece
        for picture in piece_pictures:
            picture.piece = piece
            picture.save()

        return HttpResponseRedirect('/')


class PictureCreateView(LoginRequired, CreateView):
    model = Picture

    def form_valid(self, form):
        # setting seller to be the logged in user
        form.instance.seller = self.request.user

        if "piece" in self.kwargs:
            # picture is for a piece, and not outfit
            form.instance.type = 'p'
        else:
            form.instance.type = 'o'

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
        if "piece" in self.kwargs:
            # display pictures for this seller, of type 1 (piece) and hasn't tied to a piece yet
            return Picture.objects.filter(
                seller=self.request.user,
                type='p',
                piece__isnull=True,
                display=True)
        else:
            # display pictures for this seller, of type 0 (outfit) and hasn't tied to an outfit yet
            return Picture.objects.filter(
                seller=self.request.user,
                type='o',
                outfit__isnull=True)

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
