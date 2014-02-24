from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from sell.models import Piece, Outfit


class Comment(models.Model):
    author = models.ForeignKey(User)
    comment = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now)
    # this comment can be either on an piece or outfit
    piece = models.ForeignKey(Piece, blank=True, null=True)
    outfit = models.ForeignKey(Outfit, blank=True, null=True)
