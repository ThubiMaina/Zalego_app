from django.contrib.auth import(
 	authenticate,
 	get_user_model,
 	login,
 	logout,
	)
from django.contrib.auth.models import User
from django.http import HttpResponse ,Http404, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash

from .forms import UserLoginForm,UserRegisterForm
from posts.models import UserDetail

# Create your views here.
def login_view(request):
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username ,password=password)
		
		login(request, user)
		print(request.user.is_authenticated())
		return HttpResponseRedirect("/posts/")
		#redirect
	return render(request ,"login_form.html",{"form": form,"title": title})

def register_view(request):
	title = "Register"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.is_staff=True 
		user.save()

		contact = form.cleaned_data.get('contact')
		county = form.cleaned_data.get('county')
		town = form.cleaned_data.get('town')

		UserDetail.objects.create(user=user, contact= contact, county= county, town= town)
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)

		return HttpResponseRedirect("/posts/")
	context = {
		"form":form,
		"title":title,

	}
	return render(request ,"register_form.html", context)

def logout_view(request):
	logout(request)
	messages.success(request, "You Are Now Logged out")
	return HttpResponseRedirect("/posts/")
		
		