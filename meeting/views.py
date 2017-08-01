from django.shortcuts import render
from django.views.generic import ListView, View
from django.views.generic.edit import (UpdateView, CreateView, DeleteView,
                                       FormMixin)
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import urlencode
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Room, Supplie, Reservation
from .forms import RoomForm, SupplieForm, SearchRoomForm, ReservationForm

from braces.views import (LoginRequiredMixin, SuperuserRequiredMixin)


class FormListView(FormMixin, ListView):

    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        orders = ['capacity']
        data = {'capacity__gte': self.request.POST.get('capacity', '')}

        if 'name' in self.request.POST:
            data.update({'name': self.request.POST.get('name')})
            orders.append('name')
        if 'location' in self.request.POST:
            data.update({'location': self.request.POST.get('location')})
            orders.append('location')
        if 'supplie' in self.request.POST:
            data.update({'supplie__in': self.request.POST.getlist('supplie', [])})
            orders.append('supplie')
        if data['capacity__gte'] == '':
            data['capacity__gte'] = 0
        return Room.objects.filter(**data).order_by(*orders)


class RoomListView(LoginRequiredMixin, FormListView):
    model = Room
    template_name = "meeting/meeting_list.html"
    paginate_by = 10
    context_object_name = "rooms"
    form_class = SearchRoomForm
    form2 = ReservationForm

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['second_form'] = self.form2()
        return context


class RoomEditView(SuccessMessageMixin, LoginRequiredMixin,
                   SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Room.objects.get(id=self.kwargs['pk'])
        return obj


class RoomCreateView(SuccessMessageMixin, LoginRequiredMixin,
                     SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was created successfully.")


class RoomDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                     SuperuserRequiredMixin, DeleteView):
    model = Room
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was deleted successfully.")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class SupplieListView(LoginRequiredMixin, ListView):
    model = Supplie
    template_name = "meeting/supplie_list.html"
    paginate_by = 10
    context_object_name = "supplies"

    def get_queryset(self):
        return Supplie.objects.filter(
        ).order_by(
        )


class SupplieEditView(SuccessMessageMixin, LoginRequiredMixin,
                      SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Supplie.objects.get(id=self.kwargs['pk'])
        return obj


class SupplieCreateView(SuccessMessageMixin, LoginRequiredMixin,
                        SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was created successfully.")


class SupplieDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                        SuperuserRequiredMixin, DeleteView):
    model = Supplie
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was deleted successfully.")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "meeting/reservation_list.html"
    paginate_by = 10
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.filter(
        ).order_by(
        )


class ReservationEditView(SuccessMessageMixin, LoginRequiredMixin,
                          SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/reservation_edit.html'
    form_class = ReservationForm
    success_url = reverse_lazy('reservation_list')
    success_message = _("%(name)s was saved successfully.")

    def get_object(self, queryset=None):
        obj = Reservation.objects.get(id=self.kwargs['pk'])
        return obj


class ReservationCreateView(LoginRequiredMixin, View):
    template_name = 'meeting/reservation_edit.html'
    form_class = ReservationForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("{} was reserved successfully.")

    def get_initial(self):
        initial_data = super(ReservationCreateView, self).get_initial()
        return initial_data

    def get(self, request, *args, **kwargs):
        room = Room.objects.filter(id=self.kwargs['pk'])
        status_not_reserve = ['reserved']
        if Reservation.objects.filter(
                room__status__in=status_not_reserve).exists():
            error_message = _('That room already has a reservation')
            messages.add_message(request, messages.WARNING, error_message)
            return redirect(self.success_url)

        if not room.exists():
            error_message = _('There is no room to reserve')
            messages.add_message(request, messages.ERROR, error_message)
            return redirect(reverse_lazy('meeting_list'))
        else:
            room = room.last()
        supplie = Supplie.objects.filter(room=room)
        initial_data = {'room': room}
        form = self.form_class(initial=initial_data)
        form.fields["supplie"].queryset = supplie
        context = {'form': form, 'room_object': room}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        room = Room.objects.get(id=request.POST.get('room'))
        capacity = request.POST.get('capacity')
        error = False
        if int(capacity) > room.capacity:
            message = _('Capacity must be between 0 and {} people')
            message = message.format(room.capacity)
            messages.add_message(request, messages.ERROR, message)
            error = True
        if int(capacity) <= 0:
            error = True

        if error:
            initial_data = {'room': room}
            form = self.form_class(request.POST)
            context = {'form': form, 'room_object': room}
            return render(request, self.template_name, context)

        supplies = request.POST.getlist('supplie')
        data = {
            'start': request.POST.get('start'),
            'end': request.POST.get('end'),
            'date': request.POST.get('date'),
            'capacity': capacity,
            'user': request.user,
        }

        supplies = Supplie.objects.filter(id__in=supplies)
        reservation = Reservation.objects.filter(room=room)
        if reservation.exists():
            reservation.update(**data)
            reservation = reservation.last()
        else:
            data.update({'room': room})
            reservation = Reservation.objects.create(**data)
        reservation.supplie.add(*list(supplies))
        room.status = 'reserved'
        room.save()
        self.success_message = self.success_message.format(
            reservation.room.name)
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)


class ReservationConfirmView(LoginRequiredMixin, View):
    template_name = 'meeting/reservation_edit.html'
    form_class = ReservationForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("{} was confirmed successfully.")

    def get_initial(self):
        initial_data = super(ReservationCreateView, self).get_initial()
        return initial_data

    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.filter(id=self.kwargs['pk'],
                                                 user=request.user)
        room = reservation.last().room

        if not reservation.exists():
            message = _('You do not have that room reserved')
            messages.add_message(request, messages.WARNING, message)
            return redirect(self.success_url)

        if not room.status == 'reserved':
            error_message = _('That room is not reserved')
            messages.add_message(request, messages.WARNING, error_message)
            return redirect(self.success_url)

        room.status = 'confirmed'
        room.save()
        self.success_message = self.success_message.format(room.name)
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)


class ReservationDeleteView(SuccessMessageMixin, LoginRequiredMixin,
                            SuperuserRequiredMixin, DeleteView):
    model = Reservation
    success_url = reverse_lazy('reservation_list')
    success_message = _("%(name)s was deleted successfully.")
