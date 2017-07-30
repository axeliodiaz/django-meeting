from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'location', 'capacity', 'supplie', 'status']

    def __init__(self, *args, **kwargs):
        super(RoomForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['location'].widget.attrs['class'] = 'form-control'
        self.fields['capacity'].widget.attrs['class'] = 'form-control'
        self.fields['supplie'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control'
