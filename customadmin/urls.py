from django.urls import path
from .views import (dashboard,
                    user_list,user_delete,
                    blog_list,blog_delete,admin_blog_create,admin_blog_update,
                    comment_list,comment_approved,comment_blocked,comment_delete,
                    admin_logout)

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),

    path('users/',user_list,name='admin_user_list'),
    path('users/<int:id>/',user_delete,name='admin_user_delete'),

    path('blog/',blog_list,name="admin_blog_list"),
    path('blog/<int:id>/delete',blog_delete,name='admin_blog_delete'),
    path('blogs/create/',admin_blog_create,name='admin_blog_create'),
    path('blogs/<int:id>/update/',admin_blog_update,name='admin_blog_update'),

    path('comment/',comment_list,name='admin_comment_list'),
    path('comment/<int:id>/approved',comment_approved,name='admin_comment_approved'),
    path('comment/<int:id>/blocked',comment_blocked,name='admin_comment_blocked'),
    path('comment/<int:id>/deleted',comment_delete,name='admin_comment_delete'),
    
     path('logout/', admin_logout, name='admin_logout'),

]