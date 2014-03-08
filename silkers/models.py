import uuid

from django.db import models
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

US_DRESS_SIZE = [(00, 'US 00')]
for x in range(0, 23, 2):
    US_DRESS_SIZE.append((x, 'US '+str(x)))

US_SHOE_SIZES = []
for i in range(4, 13):
    US_SHOE_SIZES.append((i, 'US '+str(i)))
    if i != 12:
        US_SHOE_SIZES.append((i+0.5, 'US ' + str(i+0.5)))


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    shoe_size = models.FloatField(choices=US_SHOE_SIZES, blank=True, null=True)
    dress_size = models.IntegerField(choices=US_DRESS_SIZE, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    state = USStateField(blank=True, null=True)
    # upload_to is not really used, it's file_storage from RegistrationWizard that's used.
    # picture = models.ImageField(upload_to="profile/%s" % (uuid.uuid4()),
    #                             blank=True,
    #                             null=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])