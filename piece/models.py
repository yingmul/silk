from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from sell.models import Piece


class Comment(models.Model):
    author = models.ForeignKey(User)
    comment = models.CharField(max_length=150)
    created = models.DateTimeField(default=timezone.now)
    piece = models.ForeignKey(Piece)
