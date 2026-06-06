from django.db import models
from blog.models import Blog
from django.contrib.auth.models import User

# Create your models here.
class Comment(models.Model):
    STATUS_CHOICES = (
        ('approved','Approved'),
        ('blocked','Blocked')
    )
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='approved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}-{self.blog.title}"
