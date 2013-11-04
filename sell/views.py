from django.views.generic import CreateView, ListView, DeleteView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from upload.serialize import serialize
from django.utils import six
from django.utils.datastructures import SortedDict
from upload.response import JSONResponse, response_mimetype
from sell.models import Picture, Outfit, Piece
from silk.views import LoginRequired
from sell.forms import SellPieceForm


TEMPLATES = {"0": "sell/sell_outfit_1.html"}
for i in range(1, settings.MAX_PIECE_SELL_FORMS + 1):
    TEMPLATES[str(i)]="sell/sell_outfit_2.html"
TEMPLATES[str(settings.MAX_PIECE_SELL_FORMS+1)]="sell/sell_outfit_preview.html"

def show_more_piece_form_condition(wizard, current_step):
    """
    Checks if the current step, the user selected 'more_pieces' to No, if true, then skip the next step
    Used in get_form_list below.
    """
    if 1 < current_step <= settings.MAX_PIECE_SELL_FORMS:
        wizard.request.session['check_for_sell_piece_pics'] = False
        cleaned_data = wizard.get_cleaned_data_for_step(unicode(current_step-1)) or {}
        if cleaned_data:
            more_pieces = cleaned_data.get('more_pieces', None)
            if more_pieces and more_pieces == u'0':
                    return False

    wizard.request.session['check_for_sell_piece_pics'] = True
    return True


class SellWizard(LoginRequired, SessionWizardView):
    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def get_form_list(self):
        """
        This method returns a form_list based on the initial form list but
        checks if there is a condition method/value in the condition_list.
        If an entry exists in the condition list, it will call/read the value
        and respect the result. (True means add the form, False means ignore
        the form)

        The form_list is always generated on the fly because condition methods
        could use data from other (maybe previous forms).

        aliu: overrides it, to call the condition function directly to pass the step it's looking for
        """
        insert_last_form = False
        form_list = SortedDict()
        for form_key, form_class in six.iteritems(self.form_list):
            #aliu: overrides to pass form_key as current step
            condition = show_more_piece_form_condition(self, int(form_key))
            if condition:
                form_list[form_key] = form_class
            else:
                #aliu: overrides to make sure we don't include the rest of the piece forms
                # if condition is ever false, that means 'more_pieces' was set to false,
                # then skip rest of the SellPieceForms, and make sure we add the last preview form
                insert_last_form = True
                break

        if insert_last_form:
            form_list[unicode(settings.MAX_PIECE_SELL_FORMS+1)] = self.form_list.value_for_index(settings.MAX_PIECE_SELL_FORMS+1)

        return form_list

    def render_done(self, form, **kwargs):
        #aliu: set session check to False to not have to check for piece pics
        self.request.session['check_for_sell_piece_pics'] = False
        return super(SellWizard, self).render_done(form, **kwargs)

    def get_context_data(self, form, **kwargs):
        self.request.session['check_for_sell_piece_pics'] = False
        context = super(SellWizard, self).get_context_data(form=form, **kwargs)
        from pprint import pprint
        pprint(self.get_all_cleaned_data())
        return context

    def get_all_cleaned_data(self):
        """
        Overwrites this method, so only in the last step, we return all the cleaned data.
        Also don't check if form is valid here, since it won't check the pictures existence check.
        """
        cleaned_data = {}
        if int(self.storage.current_step) == settings.MAX_PIECE_SELL_FORMS + 1:
            self.request.session['check_for_sell_piece_pics'] = False

            for form_key in self.get_form_list():
                form_obj = self.get_form(
                    step=form_key,
                    data=self.storage.get_step_data(form_key),
                    files=self.storage.get_step_files(form_key)
                )
                if form_obj.is_valid():
                    if isinstance(form_obj.cleaned_data, (tuple, list)):
                        cleaned_data.update({
                            'formset-%s' % form_key: form_obj.cleaned_data
                        })
                    else:
                        cleaned_data.update({
                            '%s' % form_key: form_obj.cleaned_data
                        })

        return cleaned_data

    def get_form_kwargs(self, step):
        """
        Override get_form_kwargs, to pass the request to the form's __init__ via kwargs
        """
        return {'request': self.request}

    def get(self, request, *args, **kwargs):
        self.request.session['check_for_sell_piece_pics'] = True

        #remove any pictures that did not get tied to an outfit or a piece
        Picture.objects.filter(
            seller=self.request.user,
            piece__isnull=True,
            type='p'
        ).delete()

        Picture.objects.filter(
            seller=self.request.user,
            outfit__isnull=True,
            type='o'
        ).delete()
        return super(SellWizard, self).get(request, *args, **kwargs)

    def process_step(self, form):
        # Link the pictures uploaded to the current step
        if isinstance(form, SellPieceForm):
            piece_pictures = Picture.objects.filter(
                seller=self.request.user,
                piece__isnull=True,
                type='p',
                piece_step=0
            )
            for pic in piece_pictures:
                pic.piece_step = int(self.storage.current_step)
                pic.save()

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

        # for all of the piece forms, create a Piece and tie the pictures to it
        for step, form in enumerate(form_list):
            if isinstance(form, SellPieceForm):
                piece_form_data = form.cleaned_data
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
                    type='p',
                    piece_step=step
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
        form.instance.piece_step = 0
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
                piece_step=0,
            )
                # display=True)
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
