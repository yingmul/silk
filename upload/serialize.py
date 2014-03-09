# encoding: utf-8
import mimetypes
import re
from django.core.urlresolvers import reverse


def order_name(name):
    """order_name -- Limit a text to 20 chars length, if necessary strips the
    middle of the text and substitute it for an ellipsis.

    name -- text to be limited.

    """
    name = re.sub(r'^.*/', '', name)
    if len(name) <= 20:
        return name
    return name[:10] + "..." + name[-7:]


def serialize(instance, file_attr='file'):
    """serialize -- Serialize a Picture instance into a dict.

    instance -- Picture instance
    file_attr -- attribute name that contains the FileField or ImageField

    Extra parameters set on file attribute:
    make_primary_url -- url to be used when user click on 'Make Primary' for this Picture
                -- needs to know if it's a Piece or Outfit photo in order to do the
                -- right filter inside PictureMakePrimaryView

    Extra instance parameter:
    thumbnail_url -- url retrieved from calling sorl's get_thumbnail in sell/views
                    this ensures the orientation of thumbnail shows up correct
    is_primary -- tells whether this picture is a primary photo or not
    """
    obj = getattr(instance, file_attr)
    # used in upload_tags, to show the 'Make Primary' button or not
    is_primary = getattr(instance, 'is_primary')
    thumbnail_url = getattr(instance, 'thumbnail_url')

    return {
        'url': obj.url,
        'name': order_name(obj.name),
        # 'type': mimetypes.guess_type(obj.path)[0] or 'image/png',
        #TODO DEPLOY: getting full path doesn't work with S3 storage
        'type': 'image/png',
        'thumbnailUrl': thumbnail_url,
        'size': obj.size,
        'deleteUrl': reverse('sell-delete', args=[instance.pk]),
        'deleteType': 'DELETE',
        'makePrimaryUrl': reverse(obj.make_primary_url, args=[instance.piece_step, instance.pk]),
        'isPrimary': is_primary
    }


