from django.contrib.auth.models import User
from django.db import models


class Outfit(models.Model):
    """
    Represent an outfit from seller
    """
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)


class Piece(models.Model):
    CATEGORY = [
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('tops', 'Tops'),
        ('bottoms', 'Bottoms'),
        ('dress', 'Dress'),
        ('outerwear', 'Outerwear')
    ]

    CONDITION = [
        ('nwt', 'New With Tags'),
        ('nwot', 'New Without Tags'),
        ('e', 'Excellent (like new)'),
        ('g', 'Good'),
        ('f', 'Fair'),
        ('p', 'Poor')
    ]
    price = models.DecimalField(max_digits=8, decimal_places=2)
    brand = models.CharField(max_length=50, blank=True)
    #TODO: add size -- depend on category
    category = models.CharField(choices=CATEGORY, max_length='20')
    condition = models.CharField(choices=CONDITION, max_length='5')
    outfit = models.ForeignKey(Outfit)


class Picture(models.Model):
    """
    Represents a picture of either an outfit or piece, that the seller posted
    type - determines whether this picture is for an outfit or piece
    if type=outfit, outfit FK cannot be null
    if type=piece, piece FK cannot be null
    The above restriction is not enforced in the code right now.
    """
    # type of this picture, for outfit or piece
    TYPE = [('o', 'outfit'), ('p', 'piece')]

    file = models.ImageField(upload_to="pictures")
    # Note: this really shouldn't be null, this is set after outfit is created
    outfit = models.ForeignKey(Outfit, blank=True, null=True)
    piece = models.ForeignKey(Piece, blank=True, null=True)

    # Note: this really shouldn't be null, this is so it can be set in PictureCreateView.form_valid
    seller = models.ForeignKey(User, blank=True, null=True)
    type = models.CharField(choices=TYPE, max_length=1, blank=True, null=True)
    # sets which step in the piece form, the picture was uploaded to
    piece_step = models.PositiveSmallIntegerField(default=0, blank=True)
    def __unicode__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)



