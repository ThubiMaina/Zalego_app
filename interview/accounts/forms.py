from django import forms
from django.contrib.auth import(
 	authenticate,
 	get_user_model,
 	login,
 	logout,
	)
User = get_user_model()
from django.contrib.auth.models import User
from posts.models import UserDetail

class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	def clean(self, *args ,**kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			try:
				uname = User.objects.get(username=username)
			except User.DoesNotExist:
				raise forms.ValidationError("This user does not exist")

			user = authenticate(username=username ,password=password)

			if not user:
				raise forms.ValidationError("password incorect")
	
			
			if not user.is_active:
				raise forms.ValidationError("This user is not active.")
		return super(UserLoginForm ,self).clean(*args,**kwargs)	


class UserRegisterForm(forms.ModelForm):
	contact = forms.IntegerField()
	county = forms.CharField()
	town = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model = User
		fields = [
		'username',
		'email',
		'contact',
		'county',
		'first_name',
		'last_name',
		'town',
		
		'confirm_password',
		'password',
		]

	def clean_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		if password != confirm_password:
			raise forms.ValidationError("Passwords must match")

		if len(password) < 8:
			raise forms.ValidationError("Password too short")
		return password	

	def clean_email(self):
		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email= email)
		if email_qs.exists():
			raise forms.ValidationError("This email has already been registered")
		return email	


		






