"""User forms."""

# Django
from django import forms

# Models
from users.models import Profile, User

class SignupForm(forms.Form):
    """Sign up form."""
    username = forms.CharField(
        min_length=4,
        max_length=50,
        label=False,
        widget = forms.TextInput(attrs={'placeholder':'Nombre de usuario','class': 'form-control','required': True})
        )

    password = forms.CharField(
        max_length=70,
        label=False,
        widget = forms.PasswordInput(attrs={'placeholder':'Contraseña','class': 'form-control','required': True})
    )

    password_confirmation = forms.CharField(
        min_length=4,
        max_length=70, 
        label=False,
        widget = forms.PasswordInput(attrs={'placeholder':'Confirme contraseña','class': 'form-control','required': True})
    )
    
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        label=False,
        widget = forms.TextInput(attrs={'placeholder':'Primer nombre','class': 'form-control','required': True})
        )

    last_name  = forms.CharField(
        min_length=2,
        max_length=50,
        label=False,
        widget = forms.TextInput(attrs={'placeholder':'Apellido','class': 'form-control','required': True})     
        )

    email = forms.CharField(
        min_length=6, 
        max_length=70,
        label=False,
        widget = forms.EmailInput(attrs={'placeholder':'Correo electónico','class': 'form-control','required': True}),
    )

    def clean_username(self):
        """Username must be unique."""
        username = self.cleaned_data['username']
        username_taken = User.objects.filter(username=username).exists()
        if username_taken:
            raise forms.ValidationError('El nombre se usuario ya está en uso. ☹')
        return username

    def clean_email(self):
        """Email must be unique."""
        email = self.cleaned_data['email']
        email_taken = User.objects.filter(email=email).exists()
        if email_taken:
            raise forms.ValidationError('Ya existe un usuario con ese correo electrónico.')
        return email

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return data

    def save(self):
        """Create user and profile"""
        data = self.cleaned_data
        data.pop('password_confirmation')

        user = User.objects.create_user(**data)
        profile = Profile(user=user)
        profile.save()
        

class ResetPasswordForm(forms.Form):
    username = forms.CharField(
        min_length=4,
        max_length=50,
        label=False,
        widget = forms.TextInput(attrs={'placeholder':'Nombre de usuario','class': 'form-control','required': True, 'autocomplete': 'off'})
    )

    def clean(self):
        data = super().clean()
        if not User.objects.filter(username=data['username']).exists():
            raise forms.ValidationError('El usuario no existe.')
        return data

    def get_user(self):
        username = self.cleaned_data.get('username')
        return User.objects.get(username=username)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        min_length=4,
        max_length=50,
        label=False,
        widget = forms.PasswordInput(attrs={'placeholder':'Nueva contraseña','class': 'form-control','required': True, 'autocomplete': 'off'})
    )

    password_confirmation = forms.CharField(
        min_length=4,
        max_length=50,
        label=False,
        widget = forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña','class': 'form-control','required': True, 'autocomplete': 'off'})
    )

    def clean(self):
        """Verify password confirmation match."""
        data = super().clean()

        password = data['password']
        password_confirmation = data['password_confirmation']

        if password != password_confirmation:
            raise forms.ValidationError('Las contraseñas no coinciden.')

        return data

    def get_user(self,token):
        return User.objects.get(token=token)
