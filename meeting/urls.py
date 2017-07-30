from django.conf.urls import url
from django.contrib import admin
from .views import RoomListView, RoomEditView, RoomCreateView


urlpatterns = [
    url(r'^(?P<id>\d+)/change/', RoomEditView.as_view(), name='meeting_edit'),
    url(r'^add/', RoomCreateView.as_view(), name='meeting_add'),
    url(r'^', RoomListView.as_view(), name='meeting_list'),
]
