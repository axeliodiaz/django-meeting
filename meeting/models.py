from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

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
    location = models.CharField(max_length=256)
    capacity = models.PositiveIntegerField(blank=True, null=True,
                                           help_text=_("Number of people"))
    supplie = models.ManyToManyField(Supplie, help_text=_("Select the supplies"))
    status = models.CharField(choices=STATUS, default=STATUS.available,
                              max_length=30)

    def __unicode__(self):
        return u"{}".format(self.name)


class Reservation(TimeStampedModel):
    room = models.ForeignKey(Room, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    supplie = models.ManyToManyField(Supplie)
    date = models.DateField(default=datetime.datetime.today)
    start = models.TimeField(default=timezone.now)
    end = models.TimeField(default=timezone.now)

    def __unicode__(self):
        return u"{}".format(self.room)


def reserve_room(sender, **kwargs):
    if 'created' in kwargs:
        if sender.room.status == 'available':
            sender.room.status = 'reserved'
            sender.room.save()
    # Do something
    pass
