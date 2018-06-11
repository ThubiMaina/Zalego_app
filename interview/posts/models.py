from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User


from comments.models import Comment
# Create your models here.

def upload_location(instance, filename):
	return "%s/%s" %(instance.id ,filename)
	
class UserDetail(models.Model):
	user = models.OneToOneField(User)
	contact = models.IntegerField()
	county = models.CharField(max_length=100)
	town = models.CharField(max_length=100)
	def __str__(self):
		return self.town

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title = models.CharField(max_length=100)
	content = models.TextField()
	image = models.ImageField(upload_to=upload_location,null=True , blank=False,width_field="width_field",
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('posts:detail' ,kwargs={"id": self.id})
	class Meta:
		ordering = ["-timestamp","-updated"]

	@property
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property
	def get_content_type(self):
		instance = self
		content_type =ContentType.objects.get_for_model(instance.__class__)
		return content_type	
	