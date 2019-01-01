from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token

# Create your views here.
class Main(View):
	
	def get(self, request):
		print("TEST_GET")
		csrf_token =  get_token(self.request)
		return render(request, "oldrealmwriter/home.html", {"csrf":csrf_token})
	@csrf_exempt
	def post(self, request):
		print("TEST_POST")
		print(request.POST)
		return HttpResponse('/thanks/')
		# return render(request, "oldrealmwriter/home.html")