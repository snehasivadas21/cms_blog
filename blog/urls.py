from django.urls import path
from .views import (BlogCreateView,BlogListView,BlogDetailView,BlogUpdateView,BlogDeleteView,
                    LikeCreateView,LikeDeleteView,
                    AttachmentCreateView,AttchmentListView,AttachmentDeleteView,)

urlpatterns = [
    path('create/',BlogCreateView.as_view(),name='blog_create'),
    path('list/',BlogListView.as_view(),name='blog_list'),
    path('<int:pk>/',BlogDetailView.as_view(),name='blog_detail'),
    path('<int:pk>/update/',BlogUpdateView.as_view(),name='blog_update'),
    path('<int:pk>/delete/',BlogDeleteView.as_view(),name='blog_delete'),

    path('<int:pk>/like',LikeCreateView.as_view(),name='blog_like'),
    path('<int:pk>/dislike',LikeDeleteView.as_view(),name='blog_dislike'),

    path('<int:pk>/upload',AttachmentCreateView.as_view(),name='create'),
    path('<int:pk>/list',AttchmentListView.as_view(),name='list'),
    path('<int:pk>/delete',AttachmentDeleteView.as_view(),name='delete'),
]