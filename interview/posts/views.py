from django.shortcuts import render, get_object_or_404 , redirect
from django.http import HttpResponse ,Http404, HttpResponseRedirect
from django.contrib import messages
from comments.models import Comment
from .forms import PostForm 
from .models import Post
from django.db.models import Q
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def post_create(request):
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		print(form.cleaned_data.get("title"))
		instance.save()
		messages.success(request, "successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context = {
		"form": form,
	}
	return render(request ,"post_form.html",context)

def dashboard(request):
	return render(request ,"dashboard.html")
@login_required
def post_detail(request ,id=None):#retrieve
	instance = get_object_or_404(Post,id=id)
	initial_data={
	"content_type":instance.get_content_type,
	"object_id":instance.id,
	}

	form = CommentForm(request.POST or None, initial=initial_data)

	if form.is_valid():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get('object_id')
		content_data = form.cleaned_data.get("content")
		new_comment , created = Comment.objects.get_or_create(
									user= request.user,
									content_type = content_type,
									object_id = obj_id,
									content = content_data,							
								)
		if created:
			print("worked")

	comments = instance.comments
	context = {
		"title": instance.title,
		"instance":instance,
		"comments":comments,
		"comment_form":form,
	}
	return render(request ,"post_detail.html",context)
@login_required
def post_list(request):#list items 
	queryset_list = Post.objects.all()#.order_by("-timestamp")

	query = request.GET.get("Search")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains = query)|
		    Q(content__icontains = query)|
			Q(user__first_name__icontains = query)|
			Q(user__last_name__icontains = query)
			).distinct()
	paginator = Paginator(queryset_list, 9) # Show 9 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list": queryset,
		"title": "uploads", 
		"page_request_var" : page_request_var
	}
	
	return render(request ,"post_list.html",context)

@login_required
def post_delete(request, id=None):
	instance = get_object_or_404(Post,id=id)
	if instance.user == request.user:
		instance.delete() 
		messages.success(request, "Deleted")
	else:
		messages.warning(request, "You can only delete your own post")
	return redirect('/posts/')
