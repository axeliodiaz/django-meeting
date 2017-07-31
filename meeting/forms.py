from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from .models import Room, Supplie


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


class SupplieForm(ModelForm):
    class Meta:
        model = Supplie
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SupplieForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'


class SearchRoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['capacity', 'supplie']

    def __init__(self, *args, **kwargs):
        super(SearchRoomForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', {})
        self.fields['capacity'].widget.attrs['class'] = 'form-control col-md-6'
        self.fields['supplie'].widget.attrs['class'] = 'form-control col-md-6'
        self.fields['capacity'].required = False
        self.fields['supplie'].required = False
        initial['capacity'] = 0
        kwargs['initial'] = initial
