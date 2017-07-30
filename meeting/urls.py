from django.conf.urls import url
from django.contrib import admin
from .views import RoomListView


urlpatterns = [
    url(r'^', RoomListView.as_view(), name='meeting_dashboard'),
]
