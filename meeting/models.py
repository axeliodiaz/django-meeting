from __future__ import unicode_literals

from django.db import models

from model_utils.models import TimeStampedModel, TimeFramedModel


class Supplie(models.Model):
    """Inputs for the meeting room"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u"{}".format(name)


class Room(TimeStampedModel, TimeFramedModel):
    """Conference room model"""
    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    supplie = models.ManyToManyField(Supplie)

    def __unicode__(self):
        return u"{}".format(name)
