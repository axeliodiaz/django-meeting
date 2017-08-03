# -*- coding: utf-8 -*-
import json

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.edit import (UpdateView, CreateView, DeleteView,
                                       FormMixin)
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.template.defaultfilters import urlencode
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Room, Supplie, Reservation, ReservationRequest
from .forms import RoomForm, SupplieForm, SearchRoomForm, ReservationForm

from braces.views import (LoginRequiredMixin, SuperuserRequiredMixin,
                          JSONResponseMixin)
from json_views.views import JSONDataView


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

        self.get_reservation_requests(request)
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
        queryset = Room.objects.filter(**data).order_by(*orders)
        self.update_status(queryset)
        return queryset

    def update_status(self, queryset):
        queryset = queryset.exclude(status='not available')
        # update availables
        queryset.filter(reservation__isnull=True).update(status='available')
        # update availables
        queryset.filter(reservation__isnull=False, status='available')\
            .update(status='reserved')
        return

    def get_reservation_requests(self, request):
        message = ''
        reservation_request = ReservationRequest.objects.filter(
            is_evaluated=False)
        if reservation_request.exists() and request.user.is_superuser:
            message = _("You have pending a request reservation request meeting room")
            messages.add_message(request, messages.SUCCESS, message)

        reservation_request = ReservationRequest.objects.filter(
            is_evaluated=True, user=request.user)

        for req in reservation_request:
            message = _("Your request for the {} meeting room has been rejected")
            if req.is_approved:
                message = _("Your request for the {} meeting room has been approved")
            message = message.format(req.reservation.room.name)
            messages.add_message(request, messages.SUCCESS, message)
            req.delete()
        return


class RoomListView(LoginRequiredMixin, FormListView):
    model = Room
    template_name = "meeting/meeting_list.html"
    paginate_by = 10
    context_object_name = "rooms"
    form_class = SearchRoomForm
    form2 = ReservationForm
    template_title = _('Reservation requests')

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['second_form'] = self.form2()
        context['title_page'] = self.template_title
        return context


class RoomEditView(SuccessMessageMixin, LoginRequiredMixin,
                   SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was saved successfully.")
    template_title = _('Meeting Room')

    def get_context_data(self, **kwargs):
        context = super(RoomEditView, self).get_context_data()
        context.update({'title_page': self.template_title})
        return context

    def get_object(self, queryset=None):
        obj = Room.objects.get(id=self.kwargs['pk'])
        return obj


class RoomCreateView(SuccessMessageMixin, LoginRequiredMixin,
                     SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/meeting_edit.html'
    form_class = RoomForm
    success_url = reverse_lazy('meeting_list')
    success_message = _("%(name)s was created successfully.")
    template_title = _('Meeting Room')

    def get_context_data(self, **kwargs):
        context = super(RoomCreateView, self).get_context_data()
        default_options = {'name__in': ['Pizarrón', 'Proyector']}
        context['form'] = self.form_class(
            initial={'supplie': Supplie.objects.filter(**default_options)})
        context.update({'title_page': self.template_title})
        return context

    def get_initial_data(self, default_options=None):
        initial_data = {}
        if default_options:
            supplies = Supplie.objects.filter(**default_options)
            initial_data.update({'supplie': supplies})
        return initial_data


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
    template_title = _('Supplies')

    def get_context_data(self, **kwargs):
        context = super(SupplieListView, self).get_context_data()
        context.update({'title_page': self.template_title})
        return context

    def get_queryset(self):
        return self.model.objects.filter().order_by()


class SupplieEditView(SuccessMessageMixin, LoginRequiredMixin,
                      SuperuserRequiredMixin, UpdateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was saved successfully.")
    template_title = _('Supplies')

    def get_context_data(self, **kwargs):
        context = super(SupplieEditView, self).get_context_data()
        context.update({'title_page': self.template_title})
        return context

    def get_object(self, queryset=None):
        obj = Supplie.objects.get(id=self.kwargs['pk'])
        return obj


class SupplieCreateView(SuccessMessageMixin, LoginRequiredMixin,
                        SuperuserRequiredMixin, CreateView):
    template_name = 'meeting/supplie_edit.html'
    form_class = SupplieForm
    success_url = reverse_lazy('supplie_list')
    success_message = _("%(name)s was created successfully.")
    template_title = _('Supplies')

    def get_context_data(self, **kwargs):
        context = super(SupplieCreateView, self).get_context_data()
        context.update({'title_page': self.template_title})
        return context


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
        return Reservation.objects.filter().order_by()


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


class ReservationCalendarView(LoginRequiredMixin, View):
    model = Reservation
    template_name = "meeting/calendar.html"
    form_class = ReservationForm
    template_title = _('Calendar meeting')
    success_message = "Reservation saved successfully"
    success_url = reverse_lazy('reservation_calendar')

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = {'form': self.form_class, 'title_page': self.template_title}
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            message = _('You do not have permissions to edit this reservation')
            messages.add_message(request, messages.ERROR, message)
            return redirect(self.success_url)

        id_reservation = request.POST['id_reservation']
        reservation = Reservation.objects.filter(id=id_reservation)

        action = request.POST.get('action', 'save')
        if action == 'save':
            supplies = request.POST.getlist('supplie')
            supplies = Supplie.objects.filter(id__in=supplies)

            data = {
                'start': request.POST.get('start'),
                'end': request.POST.get('end'),
                'date': request.POST.get('date'),
                'capacity': request.POST.get('capacity'),
            }
            reservation.update(**data)
            reservation = reservation.last()
            reservation.supplie.clear()
            reservation.supplie.add(*list(supplies))

        elif action == 'delete':
            reservation.delete()
            self.success_message = 'Reservation deleted successfully'

        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)


class ReservationAPIListView(LoginRequiredMixin, JSONDataView):
    model = Reservation
    context_object_name = "reservations"
    json_dumps_kwargs = {u"indent": 2}

    def get_context_data(self, **kwargs):
        context = super(ReservationAPIListView, self).get_context_data(**kwargs)
        context[self.context_object_name] = self.model.objects.filter()
        context['user'] = self.request.user
        return context


class ReservationRequestListView(LoginRequiredMixin, ListView):
    model = ReservationRequest
    template_name = "meeting/reservation_request_list.html"
    paginate_by = 10
    context_object_name = "reservation_requests"
    template_title = _('Reservation requests')
    success_url = reverse_lazy('meeting_list')

    def get_context_data(self, **kwargs):
        context = super(ReservationRequestListView, self).get_context_data()
        context.update({'title_page': self.template_title})
        return context

    def get_queryset(self):
        return self.model.objects.filter(is_evaluated=False).order_by()

    def post(self, request, *args, **kwargs):
        message = ''
        reservation_id = request.POST.get('reservation_id')
        reservation_request = ReservationRequest.objects.get(id=reservation_id)
        if 'approve' in request.POST:
            reservation_request.reservation.user = reservation_request.user
            reservation_request.reservation.save()
            reservation_request.is_approved = True
            message = "{} request has been accepted successfully"

        if 'reject' in request.POST:
            message = "{} request has been rejected successfully"
        reservation_request.is_evaluated = True
        reservation_request.save()
        message = message.format(reservation_request.user)
        success_url = {'success_url': str(self.success_url)}
        messages.add_message(request, messages.SUCCESS, message)
        return HttpResponse(json.dumps(success_url), content_type="application/json")


class ReservationRequestCreateView(SuccessMessageMixin, LoginRequiredMixin,
                                   View):
    model = ReservationRequest
    success_url = reverse_lazy('meeting_list')
    success_message = _("The administrator has been notified of your request")

    def get_reservation(self, request, queryset={}):
        queryset.update({'id': self.kwargs['pk'],
                         'user': request.user})
        obj = Reservation.objects.get(**queryset)
        return obj

    def get(self, request, *args, **kwargs):
        return redirect(self.success_url)

    def post(self, request, *args, **kwargs):
        queryset = self.model.objects.get_or_create(
            reservation=self.get_reservation(request),
            user=self.request.user
        )[0]
        print queryset
        messages.add_message(request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
