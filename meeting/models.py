from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel, TimeFramedModel
from model_utils import Choices
from model_utils.fields import StatusField


class Supplie(models.Model):
    """Inputs for the meeting room"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return u"{}".format(self.name)


class Room(models.Model):
    """Conference room model"""
    STATUS = Choices(
        _('not available'),
        _('available'),
        _('reserved'),
        _('confirmed'))

    name = models.CharField(max_length=100)
    location = models.TextField(blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    supplie = models.ManyToManyField(Supplie)
    status = models.CharField(choices=STATUS, default=STATUS.available,
                              max_length=30)

    def __unicode__(self):
        return u"{}".format(self.name)


class Reserve(TimeStampedModel, TimeFramedModel):
    room = models.ForeignKey(Room)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    supplie = models.ManyToManyField(Supplie)

    def __unicode__(self):
        return u"{}".format(self.room)
