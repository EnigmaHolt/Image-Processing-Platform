from django.conf.urls import url
from django.contrib import admin
from imageManagement import views

urlpatterns = [
    # Examples:
    url(r'^$', views.training, name='training'),
    url(r'^poll_state$', views.poll_state),
]