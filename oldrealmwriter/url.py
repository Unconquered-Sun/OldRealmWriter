from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include, url
from django.contrib import admin
from .views import Main, About

urlpatterns = [
	url(r'^$', Main.as_view(), name="Main"),
	url(r'^home/$', Main.as_view(), name="Main"),
	url(r'^about$', About.as_view(), name="About")
]
