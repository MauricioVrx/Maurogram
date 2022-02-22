"""Posts URLs."""

# Django
from django.urls import path

# Views
from posts import views

urlpatterns = [
    

    path(
        route = '', 
        view = views.PostFeedView.as_view(), 
        name='home',
        kwargs = {'type':'follow'}
    ), 

    path(
        route = 'posts/', 
        view = views.PostFeedView.as_view(), 
        name='feed',
        kwargs = {'type':'follow'}
    ),

    path(
        route = 'posts/all/', 
        view = views.PostFeedView.as_view(), 
        name='all',
        kwargs = {'type':'all'}
    ),

    path(
        route = 'posts/new/', 
        view = views.CreatePostView.as_view(), 
        name='create'
    ),

    path(
        route='post/<str:username>/<int:id>/',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
    
    path(
        route='comment/<str:username>/<int:id>/',
        view = views.comment,
        name='new_commentary'
    ),
    path(
        route='like/<str:username>/<int:id>/',
        view = views.like,
        name='like'
    ),
    
]