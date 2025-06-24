from django.urls import path
from .views import PostListView, PostDetailView, CommentCreateView, TaggedPostListView

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('tag/<slug:tag_slug>/', TaggedPostListView.as_view(), name='tagged_posts'),
]
