from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput, TextInput

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget = TextInput(attrs={'placeholder': 'Email'})
        self.fields['email'].required = True
        self.fields['username'].widget = TextInput(attrs={'placeholder': 'Username'})
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = PasswordInput(attrs={'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists() and len(email)>254:
            raise forms.ValidationError('Email already exists')
        
        return email


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class UserUpdateForm(forms.ModelForm):
    email =  forms.EmailField(required=True)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['email'].label = 'Your Email address'
        self.fields['email'].required = True


    class Meta:
        model = User
        fields = ('username', 'email')
        exclude = ('password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists() or len(email)>254:
            raise forms.ValidationError('Email already in user or is too long')
        
        return email
