from django.urls import path
from .views import CommentCreateView,CommentListView,CommentUpdateView,CommentDeleteView

urlpatterns = [
    path('create',CommentCreateView.as_view(),name='comment_create'),
    path('blogs/<int:id>/comments',CommentListView.as_view(),name='comment_list'),
    path('blogs/<int:id>/comments/update',CommentUpdateView.as_view(),name='comment_update'),
    path('blogs/<int:id>/comments/delete',CommentDeleteView.as_view(),name='comment_delete'),

]