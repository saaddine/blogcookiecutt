from django.urls import path
from . import views
# urlpatterns = [
#  path('', views.post_list, name='post_list'),
#   path('posttt/<int:pk>/', views.post_detail, name='post_detail'),
#   path('post/new/', views.post_new, name='post_new'),
#   path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
# ]
from blogcookiecutter.blog.views import PostDetailView, CreatePost, PostEditView, PostListView

app_name = "blog"
urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('posttt/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', CreatePost.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
path('feedback', views.feedbackview, name='feedback'),



]
