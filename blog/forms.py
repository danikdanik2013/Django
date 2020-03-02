from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Profile


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')


class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    bio = forms.CharField(max_length=500, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'bio', 'email', 'password1', 'password2')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'email', 'first_name', 'last_name')
