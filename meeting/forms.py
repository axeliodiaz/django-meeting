from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from .models import Room, Supplie, Reservation


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
        self.fields['capacity'].widget.attrs['class'] = 'form-control col-md-6'
        self.fields['supplie'].widget.attrs['class'] = 'form-control col-md-6'
        self.fields['capacity'].required = False
        self.fields['supplie'].required = False


class ReservationForm(ModelForm):
    READONLY_FIELDS = ['room']

    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        room = self.initial.get('room')
        self.fields['capacity'].widget.attrs['class'] = 'form-control'
        self.fields['supplie'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control mydatepicker'
        self.fields['date'].widget.attrs['id'] = 'datepicker'
        self.fields['start'].widget.attrs['class'] = 'form-control clockpicker'
        self.fields['end'].widget.attrs['class'] = 'form-control clockpicker'
        self.fields['room'].widget.attrs['class'] = 'field-disabled'

        if 'data' in kwargs:
            data = kwargs['data'].copy()
            import pdb; pdb.set_trace()
            self.prefix = kwargs.get('prefix')
            data[self.add_prefix('room')] = self.initial.get('room')
            kwargs['data'] = data

    def clean(self):
        cleaned_data = super(ReservationForm, self).clean()
        capacity = self.cleaned_data.get('capacity', 0)
        message_error = _('Capacity must be greater than 0')
        if capacity <= 0:
            self.add_error('capacity', message_error)
        return cleaned_data
