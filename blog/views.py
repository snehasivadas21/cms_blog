from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from .serializers import BlogSerializer, LikeSerializer, AttachmentSerializer
from .models import Blog, Like ,Attachment
from .forms import BlogForm, AttachmentForm
from comment.forms import CommentForm
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import PermissionDenied,ValidationError
from rest_framework.views import APIView

# Create your views here.

class BlogCreateView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BlogSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogListView(ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=BlogSerializer
    filter_backends=[SearchFilter]
    search_fields = ['title','author__username']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Blog.objects.filter(is_published=True).order_by('-created_at')

class BlogDetailView(RetrieveAPIView):
    permission_classes=[AllowAny]
    serializer_class=BlogSerializer
    queryset=Blog.objects.filter(is_published=True)

    def get_object(self):
        obj=super().get_object()
        obj.view_count+=1
        obj.save(update_fields=['view_count'])
        return obj

class BlogUpdateView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=BlogSerializer
    queryset=Blog.objects.all()

    def get_object(self):
        blog=super().get_object()
        if blog.author != self.request.user:
            raise PermissionDenied("you can edit only your own blog")
        return blog    

class BlogDeleteView(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Blog.objects.all()

    def get_object(self):
        blog=super().get_object() 
        if blog.author != self.request.user:
            raise PermissionDenied("you can delete only your own blog")
        return blog

class LikeCreateView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=LikeSerializer

    def perform_create(self, serializer):
        blog_id=self.kwargs.get('id')
        blog=get_object_or_404(Blog,id=blog_id)
        
        if Like.objects.filter(user=self.request.user,blog=blog).exists():
            raise ValidationError("One user can like a blog only once")
        serializer.save(user=self.request.user,blog=blog)

class LikeDeleteView(APIView):
    permission_classes=[IsAuthenticated]

    def delete(self,request,id):
        blog=get_object_or_404(Blog,id=id)
        like = Like.objects.filter(user=request.user,blog=blog).first()

        if not like:
            raise ValidationError("you have not liked this blog")
        like.delete()

class AttachmentCreateView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=AttachmentSerializer

    def perform_create(self, serializer):
        blog_id=self.kwargs.get('id')
        blog=get_object_or_404(Blog,id=blog_id)

        if blog.author != self.request.user:
            raise PermissionDenied("you can upload only to your own blog")
        serializer.save(blog=blog)

class AttchmentListView(ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=AttachmentSerializer
    
    def get_queryset(self):
        blog_id=self.kwargs.get('id')
        return Attachment.objects.filter(blog_id=blog_id,blog__is_published=True)

class AttachmentDeleteView(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Attachment.objects.all()

    def get_object(self):
        att=super().get_object()
        if att.blog.author != self.request.user:
            raise PermissionDenied("you can delete only to your own attachment")
        return att

#frontend requirement
def blog_list(request):
    blogs=Blog.objects.filter(is_published=True).order_by('-created_at')
    return render(request,'blog_list.html',{'blogs':blogs})    

def blog_detail(request,id):
    blog=get_object_or_404(Blog,id=id,is_published=True)

    blog.view_count += 1
    blog.save()

    comments = blog.comments.filter(status='approved').order_by('-created_at')
    attachments = blog.attachments.all()
    is_liked = Like.objects.filter(user=request.user,blog=blog).exists() if request.user.is_authenticated else False
    like_count = Like.objects.filter(blog=blog).count()
    
    return render(request,'blog_detail.html',
                  {'blog':blog,'comments':comments,'attachments':attachments,'form':CommentForm(),'is_liked':is_liked,'like_count':like_count})

@login_required
@never_cache
def my_blogs(request):
    blogs = Blog.objects.filter(author=request.user).order_by('-created_at')
    return render(request,'my_blogs.html',{'blogs':blogs})

@login_required
@never_cache
def blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        
        if form.is_valid():
            blog = form.save(commit=False)

            blog.author = request.user

            blog.save()
            
            messages.success(request,'Blog created successfully')
            return redirect('blog_detail',id=blog.id) 
    else:
        form = BlogForm()
    return render(request,'blog_create.html',{'form':form})   

@login_required
@never_cache
def blog_update(request,id):
    blog = get_object_or_404(Blog,id=id,author=request.user)

    if request.method == 'POST':
        form = BlogForm(request.POST,instance=blog)

        if form.is_valid():
            blog = form.save(commit=False)

            blog.author = request.user

            blog.save()

            messages.success(request,'Blog updated successfully')
            return redirect('blog_detail',id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request,'blog_update.html',{'form':form,'blog':blog})

@login_required
@never_cache
def blog_delete(request,id):
    blog = get_object_or_404(Blog,id=id,author=request.user)

    if request.method == 'POST':
        blog.delete()

        messages.success(request,'Blog deleted successfully')
        return redirect('blog_list')
    return render(request,'blog_delete.html',{'blog':blog})

@login_required
@never_cache
def attachment_upload(request,id):
    if request.user.is_staff:
       blog = get_object_or_404(Blog, id=id)
    else:
        blog = get_object_or_404(Blog,id=id,author=request.user)

    if request.method == 'POST':
        form = AttachmentForm(request.POST,request.FILES)

        if form.is_valid():
            attachment = form.save(commit=False) 

            attachment.blog = blog

            attachment.save()

            messages.success(request,'Attachment added successfully')
            return redirect('blog_detail',id=blog.id)
    else:
        form=AttachmentForm()    
    return render(request,'attachment_upload.html',{'form':form,'blog':blog}) 

@login_required
def attachment_delete(request,id):
    attachment = get_object_or_404(Attachment,id=id)

    if attachment.blog.author != request.user:
        raise PermissionDenied("you can delete only your own attachment")
    
    blog_id = attachment.blog.id

    if request.method == 'POST':
        attachment.delete()

        messages.success(request,'Attachment deleted successfully')
    return redirect('blog_detail',id=blog_id)    

@login_required
def like_blog(request,id):
    blog = get_object_or_404(Blog,id=id)
    
    exising_like  = Like.objects.filter(user=request.user,blog=blog).exists()
    if exising_like:
       like = Like.objects.get(user=request.user,blog=blog)
       like.delete()
    else:
       Like.objects.create(user=request.user,blog=blog)   
    return redirect('blog_detail',id=id)