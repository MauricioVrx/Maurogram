"""Posts views."""
#Django
from django.db.models.expressions import RawSQL
from django.http import request
from users.models import Follow
from django.urls import reverse_lazy
from django.contrib.auth.mixins  import LoginRequiredMixin #investigar mixin
from django.views.generic import ListView, DetailView, CreateView #investigar
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.db import connections
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Forms
from posts.forms import PostForm

# Models
from posts.models import Post, Like, Comment


class PostFeedView(LoginRequiredMixin, ListView):
    """Return follow's published posts."""
    
    template_name = 'posts/feed.html'
    model = Post
    ordering = ('-created',)
    paginate_by = 2
    context_object_name = 'posts'


    def get_queryset(self):
        level = self.kwargs['type']
        if level == 'all':
            queryset = Post.objects.raw('SELECT p.* FROM posts_post as p, users_follow as f WHERE f.profile_id = ' + str(self.request.user.id) + ' AND f.user = p.user_id ORDER BY p.id DESC ')
        else:
            queryset = Post.objects.all().order_by('-created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limit_comment'] = 2
        return context
        # page_number = self.request.GET.get('page')
        # print(str(self.paginate_by)+" and "+str(page_number))



class PostDetailView(LoginRequiredMixin, DetailView):
    """Posts detail view."""

    template_name = 'posts/detail.html'
    slug_field = 'id'
    slug_url_kwarg = 'id'
    queryset = Post.objects.all()
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['limit_comment'] = 0
        return context
   

class CreatePostView(LoginRequiredMixin, CreateView):
    """Create a new post."""

    template_name = 'posts/new.html'
    form_class = PostForm
    success_url = reverse_lazy('posts:feed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user']    = self.request.user
        context['profile'] = self.request.user.profile
        return context

@login_required
def like(request, username, id):
    """Like post."""
    
    profile= request.user
    post = Post.objects.filter(id=id).first()
    instance  = Like.objects.filter(profile=profile,post=post).first()

    # Search if Like instace exist or make a new one
    if instance:
        like = instance
    else:
        like = Like()

    like.post= post
    like.profile = profile

    # Set status of Like instance
    if instance:
        if instance.status == 'n':
            like.status = 'l'
        else:
            like.status = 'n'
    else:
        like.status = 'l'

    like.save()
    return redirect("posts:detail", username=username, id=id)

@login_required
def comment(request, username, id):
    """Like post."""
    
    profile= request.user
    post = Post.objects.filter(id=id).first()
    
    comment = Comment()

    comment.comment = request.POST['commentary']
    comment.status  = 'a'
    comment.post = post
    comment.user = profile
    comment.save()

    return redirect("posts:detail", username=username, id=id)

@register.filter
def get_value(dictionary, key):
    """Return a value from dict"""
    return dictionary[key]

@register.filter
def get_likes(post):
    return Like.objects.filter(post=post, status= 'l').count()

@register.filter
def get_own_like(post, profile):
    val = Like.objects.values('status').filter(post=post, status= 'l', profile=profile).first()
    return val['status']

@register.filter
def get_comments(post,limit_comment):
    select_c = "SELECT c.id, c.comment, c.status, c.created, u.username as username, p.picture as picture, u.first_name, u.last_name "
    form_c   = "FROM posts_comment as c, users_user as u, users_profile as p "
    where_c  = "WHERE c.status LIKE 'a' AND c.user_id = u.id AND p.user_id = u.id "
    limit_text = ""
    if limit_comment > 0:
        limit_text = "LIMIT "+ str(limit_comment)
    comments = Comment.objects.raw(select_c + form_c + where_c + ' AND c.post_id = '+str(post.id)+' ORDER BY c.id DESC '+limit_text) 
    return comments

@register.filter
def get_count_all_comments(post, descount):
    if descount > 0:
        post_count_comment = Comment.objects.filter(post=post, status='a').count()-descount
        return post_count_comment
    else:
        return 0