from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from blog.models import Blog
from comment.models import Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.cache import never_cache
from blog.forms import BlogForm

User = get_user_model()

# Create your views here.
@login_required
@never_cache
def dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    total_users = User.objects.all().count()
    total_blogs = Blog.objects.all().count()
    total_comments = Comment.objects.all().count()

    context = {
        'total_users':total_users,
        'total_blogs':total_blogs,
        'total_comments':total_comments,
    }
    return render(request,'admin/admin_dashboard.html',context)

@login_required
@never_cache
def user_list(request):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    users = User.objects.all().order_by('-date_joined')
    return render(request,'admin/user_list.html',{'users':users})

@login_required
@never_cache
def user_delete(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    user=get_object_or_404(User,id=id)

    if user.is_superuser and user == request.user:
        messages.error(request,"Cannot delete superuser")
        return redirect('admin_user_list')
    
    if request.method == 'POST':
        user.delete()

        messages.success(request,'User deleted successfully')
        return redirect('admin_user_list')
    return render(request,'admin/user_delete.html',{'user':user})

@login_required  
@never_cache     
def blog_list(request):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    blogs=Blog.objects.all().order_by('-created_at')
    return render(request,'admin/blog_list.html',{'blogs':blogs})  

@login_required
@never_cache
def blog_delete(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    blog = get_object_or_404(Blog,id=id)

    if request.method == 'POST':
        blog.delete()

        messages.success(request,'Blog deleted successfully')
        return redirect('admin_blog_list')
    
@login_required
@never_cache
def admin_blog_create(request):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")

    if request.method == 'POST':
        form =  BlogForm(request.POST)

        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()

            messages.success(request,'Blog creted succesfully')
            return redirect('admin_blog_list')   
    else:
        form = BlogForm()

    return render(request,'admin/blog_create.html',{'form':form})

@login_required
@never_cache
def admin_blog_update(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")

    blog = get_object_or_404(Blog,id=id)

    if request.method == 'POST' :
        form = BlogForm(request.POST,instance=blog)

        if form.is_valid():
            blog=form.save()

            messages.success(request,'Blog updated successfully')
            return redirect('admin_blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request,'admin/blog_update.html',{'form':form,'blog':blog})            

@login_required
@never_cache
def comment_list(request):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    comments = Comment.objects.all().order_by('-created_at')
    return render(request,'admin/comment_list.html',{'comments':comments})

@login_required
@never_cache
def comment_approved(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    comment = get_object_or_404(Comment, id=id)
    comment.status = 'approved'
    comment.save()
    messages.success(request,'comment approved succesfully')
    return redirect('admin_comment_list')

@login_required
@never_cache
def comment_blocked(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    comment = get_object_or_404(Comment, id=id)
    comment.status = 'blocked'
    comment.save()
    messages.success(request, 'comment blocked successfully.')
    return redirect('admin_comment_list')

@login_required
@never_cache
def comment_delete(request,id):
    if not request.user.is_staff:
        raise PermissionDenied("Admin access required")
    
    comment = get_object_or_404(Comment,id=id)

    if request.method == 'POST':
        comment.delete()

        messages.success(request,'Comment deleted successfully')
        return redirect('admin_comment_list')

@login_required
def admin_logout(request):
    logout(request)
    return redirect('login')

