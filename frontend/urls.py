from django.urls import path
from blog.views import blog_list,blog_detail,my_blogs,blog_create,blog_update,blog_delete,attachment_upload,attachment_delete,like_blog
from comment.views import add_comment,update_comment,delete_comment
from user.views import register_view,login_view,logout_view

urlpatterns = [    
    path('', blog_list, name='blog_list'),
    path('blog/<int:id>/', blog_detail, name='blog_detail'),
    path('my-blogs/', my_blogs, name='my_blogs'),
    path('blog/create/', blog_create, name='blog_create'),
    path('blog/<int:id>/update',blog_update,name='blog_update'),
    path('blog/<int:id>/delete',blog_delete,name='blog_delete'),

    path('blog/<int:id>/upload/',attachment_upload,name='attachment_upload'),
    path('attachment/<int:id>/delete/',attachment_delete,name='attachment_delete'),

    path('blog/<int:id>/like',like_blog, name='like_blog'),

    path('blog/<int:id>/add_comment/',add_comment,name="add_comment"),
    path('blog/<int:id>/update_comment/',update_comment,name="update_comment"),
    path('blog/<int:id>/delete_comment/',delete_comment,name="delete_comment"),

    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]