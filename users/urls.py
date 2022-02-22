"""User URLs"""

# Django
from django.urls import path
from django.views.generic import TemplateView
# from django.views.generic import TemplateView

# Views
from users import views

urlpatterns = [

    # Management
    path(
        route = 'login/',
        view = views.LoginView.as_view(),
        name='login'
    ),

    path(
        route = 'logout/',    
        view = views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        route = 'signup/',    
        view = views.SignupView.as_view(),
        name='signup'
    ),

    path(
        route = 'me/profile/', 
        view = views.UpdateProfileView.as_view(),
        name='update_profile'
    ),
    path(
        route='follow/<str:username>/',
        view = views.follow,
        name='follow'
    ),

    path(
        route = 'reset_password/', 
        view = views.ResetPasswordView.as_view(),
        # view = views.func,
        name='reset_password'
    ),

    path(
        route = 'change_password/<str:token>', 
        view = views.ChangePasswordView.as_view(),
        name='change_password'
    ),

    path(
        route='search/',
        view = views.search_user,
        name='search'
    ),

    # Posts
    path(
        route='profile/<str:username>/',
        # view = TemplateView.as_view(template_name='users/detail.html'),
        view = views.UserDetailView.as_view(),
        name='detail'
    ),

    


    

]
