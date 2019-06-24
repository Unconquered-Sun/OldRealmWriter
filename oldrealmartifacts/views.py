from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
class Main(View):
	def get(self, request):
		return render(request, "")