from django.contrib.auth.models import User
from django.db import models
from sorl.thumbnail import delete, ImageField
from django.utils import timezone


class Outfit(models.Model):
    """
    Represent an outfit from seller
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=500, blank=True)
    num_likes = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(default=timezone.now)


# dictionary used in Piece model and in SellPreviewForm
condition_display = {
    'nwt': 'New With Tags',
    'nwot': 'New Without Tags',
    'e': 'Excellent (like new)',
    'g': 'Good',
    'f': 'Fair',
    'p': 'Poor'
}

class Piece(models.Model):
    CATEGORY = [
        ('Shoes', 'Shoes'),
        ('Accessories', 'Accessories'),
        ('Tops', 'Tops'),
        ('Bottoms', 'Bottoms'),
        ('Dress', 'Dress'),
        ('Outerwear', 'Outerwear')
    ]

    CONDITION = [
        ('nwt', condition_display['nwt']),
        ('nwot', condition_display['nwot']),
        ('e', condition_display['e']),
        ('g', condition_display['g']),
        ('f', condition_display['f']),
        ('p', condition_display['p'])
    ]

    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=50)
    # TODO: (nice to have) make size into a drop down field when category change values
    size = models.CharField(max_length=5)
    category = models.CharField(choices=CATEGORY, max_length=20)
    condition = models.CharField(choices=CONDITION, max_length=5)
    description = models.CharField(max_length=500, blank=True)
    outfit = models.ForeignKey(Outfit)


class Picture(models.Model):
    """
    Represents a picture of either an outfit or piece, that the seller posted
    type - determines whether this picture is for an outfit or piece
    if type=outfit, outfit FK cannot be null
    if type=piece, piece FK cannot be null
    The above restriction is not enforced in the code right now.

    The following fields really shouldn't be nullable, they need to be because the values are being
    set later in the PictureCreateView's form_valid:
        thumbnail
        outfit
        seller
        type
    """
    class Meta:
        ordering = ['-is_primary']

    # type of this picture, for outfit or piece
    TYPE = [('o', 'outfit'), ('p', 'piece')]

    file = ImageField(upload_to="pictures")

    # field for sorl's thumbnail url
    thumbnail_url = models.URLField(blank=True)
    # if not null, picture is for this outfit
    outfit = models.ForeignKey(Outfit, blank=True, null=True)
    # if not null, picture is for this piece
    piece = models.ForeignKey(Piece, blank=True, null=True)

    is_primary = models.BooleanField(default=False)
    seller = models.ForeignKey(User, blank=True, null=True)
    type = models.CharField(choices=TYPE, max_length=1, blank=True)
    # sets which step in the piece form, the picture was uploaded to (default=0 means it hasn't been tied to a step yet)
    piece_step = models.PositiveSmallIntegerField(default=0, blank=True)

    def __unicode__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        delete(self.file)
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
