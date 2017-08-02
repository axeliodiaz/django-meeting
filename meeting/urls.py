from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import TemplateView
from .views import (RoomListView, RoomEditView, RoomCreateView,
                    RoomDeleteView, SupplieListView, SupplieEditView,
                    SupplieCreateView, SupplieDeleteView, ReservationEditView,
                    ReservationDeleteView, ReservationCreateView,
                    ReservationListView, ReservationConfirmView,
                    ReservationAPIListView, ReservationCalendarView)


urlpatterns = [
    url(r'^supplie/(?P<pk>\d+)/change/', SupplieEditView.as_view(),
        name='supplie_edit'),
    url(r'^supplie/(?P<pk>\d+)/delete/', SupplieDeleteView.as_view(),
        name='supplie_delete'),
    url(r'^supplie/add/', SupplieCreateView.as_view(), name='supplie_add'),
    url(r'^supplie/list/', SupplieListView.as_view(), name='supplie_list'),
    url(r'^reservation/(?P<pk>\d+)/change/', ReservationEditView.as_view(),
        name='reservation_edit'),
    url(r'^reservation/(?P<pk>\d+)/delete/', ReservationDeleteView.as_view(),
        name='reservation_delete'),
    url(r'^reservation/(?P<pk>\d+)/add/', ReservationCreateView.as_view(),
        name='reservation_add'),
    url(r'^reservation/(?P<pk>\d+)/confirm/', ReservationConfirmView.as_view(),
        name='reservation_confirm'),
    url(r'^reservation/list/', ReservationListView.as_view(),
        name='reservation_list'),
    url(r'^api/reservation/', ReservationAPIListView.as_view(),
        name='reservation_api_calendar'),
    url(r'^reservation/calendar/', ReservationCalendarView.as_view(),
        name='reservation_calendar'),
    url(r'^(?P<pk>\d+)/change/', RoomEditView.as_view(), name='meeting_edit'),
    url(r'^(?P<pk>\d+)/delete/', RoomDeleteView.as_view(),
        name='meeting_delete'),
    url(r'^add/', RoomCreateView.as_view(), name='meeting_add'),
    url(r'^', RoomListView.as_view(), name='meeting_list'),
]
