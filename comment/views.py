from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializers import CommentSerializer
from .models import Comment
from .forms import CommentForm
from blog.models import Blog
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class CommentCreateView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CommentSerializer

    def perform_create(self, serializer):
        blog_id = self.kwargs.get('id')
        blog = get_object_or_404(Blog,id=blog_id)
        serializer.save(author=self.request.user,blog=blog)

class CommentListView(ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=CommentSerializer
    pagination_class=PageNumberPagination

    def get_queryset(self):
        return Comment.objects.filter(blog_id=self.kwargs['blog_id'],status='approved').order_by('-created_at')

class CommentUpdateView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CommentSerializer
    queryset = Comment.objects.all()

    def get_object(self):
        comment = super().get_object()  
        if comment.author != self.request.user:
            raise PermissionDenied("you can edit only your own comment")
        return comment  

class CommentDeleteView(DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Comment.objects.all()

    def get_object(self):
        comment = super().get_object()
        if comment.author != self.request.user:
            raise PermissionDenied("you can delete only your own comment")
        return comment
    

#frontend requirement
@login_required
def add_comment(request,id):
    blog=get_object_or_404(Blog,id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            
            comment.blog=blog
            comment.author=request.user
            comment.save()

            messages.success(request,'Comment added successfully')
            return redirect('blog_detail',id=blog.id)
        return render(request,'blog_detail.html',{'form':form,'blog':blog})

@login_required
def update_comment(request,id):
    comment = get_object_or_404(Comment,id=id,author=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST,instance=comment)

        if form.is_valid():
            form.save()

            messages.success(request,'Comment updated successfully')
            return redirect('blog_detail',id=comment.blog.id)
    else:
        form = CommentForm(instance=comment)
    return render(request,'comment_update.html',{'form':form,'comment':comment})    

@login_required
def delete_comment(request,id):
    comment = get_object_or_404(Comment,id=id,author=request.user)

    blog_id = comment.blog.id

    if request.method == 'POST':
        comment.delete()

        messages.success(request,'Comment deleted successfully')
        return redirect('blog_detail',id=blog_id)
    return redirect(request,'blog_detail.html',{'comment':comment})        