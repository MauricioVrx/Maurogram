"""Users views."""

# Django
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


#from django.contrib.auth.forms import AuthenticationForm

# Models
from users.models import Profile, User
from posts.models import Post
from users.models import Follow

# Forms
from users.forms import  SignupForm, ResetPasswordForm, ChangePasswordForm

# Utilities
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from maurogram import settings
import uuid


class LoginView(auth_view.LoginView):
    """Login view."""
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('posts:feed'))
        return self.render_to_response(self.get_context_data())


class UserDetailView(LoginRequiredMixin, DetailView): #importante
    """User detail view."""
    template_name = 'users/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username' #se basa en el nombre de <str:username> que se encuentra en users/urls.py
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add users's posts to context."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        context['posts']     = Post.objects.filter(user=user).order_by('-created')
        context['follow']    = Follow.objects.filter(profile=self.request.user.id , user=user.id).first()
        context['followers'] = Follow.objects.filter(user=user.id, status='f').count()
        context['following'] = Follow.objects.filter(profile=user.id, status='f').count()
        context['my_posts']  = Post.objects.filter(user=user).count

        return context


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    template_name = 'users/update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']

    def get_object(self):
        """Return user's profile"""
        return self.request.user.profile

    def get_success_url(self):
        """Return user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username':username})


class SignupView(FormView):
    """Users sign up view."""

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('posts:feed'))
        return self.render_to_response(self.get_context_data())

    template_name = 'users/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        """Save form data."""
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return str(self.success_url)


class LogoutView(LoginRequiredMixin, auth_view.LogoutView):
    """Logout view."""
    template_name = 'users/login.html'

    
def follow(request, username):
    """Follow user."""
    
    profile_follow = User.objects.filter(username=username).first()
    profile= request.user
    user=profile_follow.id

    account  = Follow.objects.filter(profile=profile,user=user).first()

    if account:
        follow = account
        if account.status == 'n':
            follow.status = 'f'
        else:
            follow.status = 'n'
    else:
        follow = Follow()
        follow.status = 'f'


    follow.user= user
    follow.profile = profile

    follow.save()

    return redirect("users:detail", username=username)


class ResetPasswordView2(FormView):
    """Reset password view."""

    template_name = 'accounts/resetpwd.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('posts:home')

    def sent_email(self, user):
        context = {
            'user': user,
            'link_resetpwd': '',
            'link_home': ''
        }
    
        template = get_template('accounts/send_email.html')
        content = template.render(context)
        

        email = EmailMultiAlternatives(
            'Reseteo de contraseña - Maurogram', #title
            'Maurogram', #Asunto
            settings.EMAIL_HOST_USER, #Quien envía
            [user.email]
        )

        email.attach_alternative(content, 'text/html')
        email.send()

    def form_valid(self, form):
        """."""
        pass
        return super().form_valid(form)

    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            form  = ResetPasswordForm(request.POST) # or self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.sent_email(user)
            else:
                data['error'] = form.errors
                
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
        #return self.form_valid(form)


class ResetPasswordView(FormView):
    """Reset password view."""

    template_name = 'accounts/resetpwd.html'
    form_class = ResetPasswordForm

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('posts:feed'))
        return self.render_to_response(self.get_context_data())
    
    def send_email_reset_pwd(self, user):
        data = {}
        try:
            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email_to = user.email
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = 'Reseteo de contraseña - Maurogram'

            content = render_to_string('accounts/send_email.html', {
                'user': user,
                'link_resetpwd': f'http://{URL}/users/change_password/{str(user.token)}',
                'link_home': f'http://{URL}',
            })
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to, 
                                mensaje.as_string())
        except Exception as e:
            data['error'] = str(e)
        return data


    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            form  = ResetPasswordForm(request.POST) # or self.get_form()
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user) #Para enviar mail
                mail = User.objects.values('email').filter(username=user.username).first()
                return render(request, 'accounts/mail_sended.html', {'mail':mail})
            else:
                data['error'] = form.errors
                
        except Exception as e:
            data['error'] = str(e)
        return self.form_invalid(form)


class ChangePasswordView(FormView):
    """Change password view."""

    template_name = 'accounts/changepwd.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('posts:home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('posts:feed'))
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    def form_valid(self, form):
        """Save form data."""
        return super().form_valid(form)
        

    def post(self, request, *arg, **kwargs):
        data = {}
        try:
            form  = ChangePasswordForm(request.POST) # or self.get_form()
            if form.is_valid():
                user = form.get_user(self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token= uuid.uuid4() #Token   # or ""
                user.save()
                return render(request, 'accounts/changedpwd.html', {'username':user.username})
            else:
                data['error'] = form.errors                
        except Exception as e:
            data['error'] = str(e)
        return self.form_invalid(form)


### Send a simple email ##########
@login_required
def sent_email(mail):
    context = {'mail': mail}
    
    template = get_template('accounts/correo.html')
    content = template.render(context)
    

    email = EmailMultiAlternatives(
        'Un correo de prueba', #title
        'Maurogram', #Asunto
        settings.EMAIL_HOST_USER, #Quien envía
        [mail]
    )

    email.attach_alternative(content, 'text/html')
    email.send()
@login_required
def func(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        sent_email(mail)

    return render(request, 'accounts/index.html', {})
    # return redirect("posts:feed")
###################################
@login_required
def search_user(request):
    """Search user in navbar."""
    if request.method == 'POST':
        username = request.POST['username']
        user  = User.objects.filter(username=username).first()
        if not user:
            return render(request, "users/user_not_found.html", {'username':username})

        return redirect("users:detail", username=username)   
    return redirect("posts:feed")
