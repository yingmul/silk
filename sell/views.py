from django.views.generic import CreateView, ListView, DeleteView
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from upload.serialize import serialize
from django.utils import six
from django.utils.datastructures import SortedDict
from django.views.generic.detail import BaseDetailView, SingleObjectTemplateResponseMixin
from sorl.thumbnail import get_thumbnail
from upload.response import JSONResponse, response_mimetype
from sell.models import Picture, Outfit, Piece, condition_display
from silk.views import LoginRequired
from sell.forms import SellPieceForm

TEMPLATES = {"0": "sell/sell_outfit.html"}
for i in range(1, settings.MAX_PIECE_SELL_FORMS + 1):
    TEMPLATES[str(i)]="sell/sell_piece.html"
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

    def get(self, request, *args, **kwargs):
        self.request.session['check_for_sell_piece_pics'] = True
        return super(SellWizard, self).get(request, *args, **kwargs)

    def render_done(self, form, **kwargs):
        #aliu: set session check to False to not have to check for piece pics
        self.request.session['check_for_sell_piece_pics'] = False
        return super(SellWizard, self).render_done(form, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super(SellWizard, self).get_context_data(form=form, **kwargs)

        # only call get_cleaned_data when it's last step, for preview
        if int(self.storage.current_step) == settings.MAX_PIECE_SELL_FORMS + 1:
            context["preview"] = self.get_all_cleaned_data()
        return context

    def get_all_cleaned_data(self):
        """
        Overwriting this to skip checking photo existence.
        And also set the key in cleaned_data based on form_key, so we can have one dict for each piece form
        Returns data in this format:
        {
            "outfit": {"name": , "description": , "pictures": [list of outfit pic urls],
            "pieces":
            [{"price", "brand", "category", "condition", "pictures": [list of piece pic urls]}]
        }
        """
        self.request.session['check_for_sell_piece_pics'] = False

        preview_data = {}
        pieces_data = []
        for form_key in self.get_form_list():
            form_obj = self.get_form(
                step=form_key,
                data=self.storage.get_step_data(form_key),
                files=self.storage.get_step_files(form_key)
            )
            if form_obj.is_valid():
                step = int(form_key)
                if step == 0:
                    # this is outfit form
                    preview_data["outfit"] = form_obj.cleaned_data

                    outfit_pictures = Picture.objects.filter(
                        seller=self.request.user,
                        outfit__isnull=True,
                        type='o')
                    pic_urls = []
                    for pic in outfit_pictures:
                        pic_urls.append(pic.thumbnail_url)
                    preview_data["outfit"]["pictures"] = pic_urls
                else:
                    piece = form_obj.cleaned_data
                    # convert condition to its display value
                    piece["condition_display"] = condition_display[piece["condition"]]
                    piece["number"] = step
                    piece_pictures = Picture.objects.filter(
                        seller=self.request.user,
                        piece__isnull=True,
                        type='p',
                        piece_step=step
                    )
                    piece_pic_urls = []
                    for pic in piece_pictures:
                        piece_pic_urls.append(pic.thumbnail_url)
                    piece["pictures"] = piece_pic_urls
                    pieces_data.append(piece)

        preview_data["pieces"] = pieces_data

        return preview_data

    def get_form_kwargs(self, step):
        """
        Override get_form_kwargs, to pass the request to the form's __init__ via kwargs
        """
        return {'request': self.request}

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
                    description=piece_form_data['description'],
                    size=piece_form_data['size'],
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


def get_current_photos(is_piece, user, curr_step):
    if is_piece:
        # display pictures for this seller, of type 'p' (piece) and hasn't tied to a piece yet:
        # step = curr_step: photos that were uploaded in current step for piece forms
        return Picture.objects.filter(
            seller=user,
            type='p',
            piece__isnull=True,
            piece_step=curr_step
        )
    else:
        # display pictures for this seller, of type 'o' (outfit) and hasn't tied to an outfit yet
        return Picture.objects.filter(
            seller=user,
            type='o',
            outfit__isnull=True)


def make_primary_photo_false(photo_filter):
    if photo_filter.count() > 1:
        #TODO: convert this to log with ERROR
        print 'In PictureMakePrimaryView, found number of old primary photo greater than 1: ' \
            + str(photo_filter.count())

    for photo in photo_filter:
        photo.is_primary = False
        photo.save()


class PictureCreateView(LoginRequired, CreateView):
    model = Picture

    def form_valid(self, form):
        # setting seller to be the logged in user
        form.instance.seller = self.request.user
        if "piece" in self.kwargs:
            # picture is for a piece, and not outfit
            form.instance.type = 'p'
            make_primary_url = 'sell-piece-make-primary'
            form.instance.piece_step = self.kwargs['step']
        else:
            form.instance.type = 'o'
            make_primary_url = 'sell-make-primary'
            form.instance.piece_step = 0

        self.object = form.save()

        # save form again to set the thumbnail_url
        thumbnail = get_thumbnail(
            self.object,
            settings.SORL_THUMBNAIL_SIZE,
            crop=False,
            quality=99)

        form.instance.thumbnail_url = thumbnail.url
        self.object = form.save()

        # pass the appropriate make_primary_url for this object (Picture)
        self.object.file.make_primary_url = make_primary_url
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        # TODO: fix this to log it as an error
        # An error occurred from the program's point of view (not user)
        from pprint import pprint
        pprint(form.errors)
        return super(PictureCreateView, self).form_invalid(form)


class PictureDeleteView(LoginRequired, DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureMakePrimaryView(LoginRequired, SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Picture

    def post(self, *args, **kwargs):
        # make the original primary Picture (if there is any) to not a primary photo
        curr_step = int(kwargs['step'])

        existing_primary_photos = \
            get_current_photos("piece" in kwargs, self.request.user, curr_step)\
                .filter(is_primary=True)

        make_primary_photo_false(existing_primary_photos)

        # make this Picture a primary photo
        self.object = self.get_object()
        self.object.is_primary = True
        self.object.save()

        response = JSONResponse(True, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(LoginRequired, ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        curr_step = 0
        if "piece" in self.kwargs:
            make_primary_url = 'sell-piece-make-primary'
            curr_step = int(self.kwargs['step'])
        else:
            make_primary_url = 'sell-make-primary'

        files = []
        curr_photos = \
            get_current_photos("piece" in self.kwargs, self.request.user, curr_step)\
                .order_by('-is_primary')
        for p in curr_photos:
            p.file.make_primary_url = make_primary_url
            files.append(serialize(p))

        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
