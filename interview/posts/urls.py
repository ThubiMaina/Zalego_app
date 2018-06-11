from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.post_list, name='list'),
	url(r'^create/$',views.post_create, name='post_create'),
	url(r'^(?P<id>\d+)/$',views.post_detail, name='detail'),
	url(r'^(?P<id>\d+)/delete/$',views.post_delete, name='post_delete')
	]