from __future__ import unicode_literals
from django.db import models
import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'documents'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    filename = instance.description
    return os.path.join(upload_to, filename)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to=path_and_rename)
    uploaded_at = models.DateTimeField(auto_now_add=True)
