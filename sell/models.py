from django.contrib.auth.models import User
from django.db import models


class Outfit(models.Model):
    """
    Represent an outfit from seller
    """
    user = models.ForeignKey(User, blank=True, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)


class Picture(models.Model):
    file = models.ImageField(upload_to="pictures")
    slug = models.SlugField(max_length=50, blank=True)
    outfit = models.ForeignKey(Outfit, blank=True, null=True)

    def __unicode__(self):
        return self.file.name

    @models.permalink
    def get_absolute_url(self):
        return ('sell-new', )

    def save(self, *args, **kwargs):
        self.slug = self.file.name
        super(Picture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        super(Picture, self).delete(*args, **kwargs)


