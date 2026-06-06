from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .serializers import CommentSerializer, CommentModerationSerializer
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

class CommentModerationView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CommentModerationSerializer
    queryset=Comment.objects.all()

    def get_object(self):
        comment = super().get_object()
        if not self.request.user.is_staff:
            raise PermissionDenied("only admin can moderate the comment")
        return comment

#frontend requirement
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
