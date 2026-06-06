from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=50)
    content= models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  

class Attachment(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='attachments')
    file = models.FileField(upload_to='blog_attchments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)