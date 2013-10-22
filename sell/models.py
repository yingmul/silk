import uuid
import os

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models


class ImageAttachment(models.Model):
    """A tag on an item."""
    file = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'sell', str(uuid.uuid4())[:8]))
    thumbnail = models.ImageField(upload_to=os.path.join(settings.MEDIA_ROOT, 'sell', 'tn', str(uuid.uuid4())[:8]))
    creator = models.ForeignKey(User, related_name='image_clothes')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return self.file


class Picture(models.Model):
    file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)
    creator = models.ForeignKey(User, blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('sell-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """delete -- Remove to leave file."""
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)
