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


class Email(forms.EmailField):
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError(
                "This email is already registered.")
        except User.DoesNotExist:
            return value


class SignUpForm(UserCreationForm):
    email = Email()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Profile
        email = Email()
        fields = ('email', 'first_name', 'last_name')


class EmailEdit(forms.ModelForm):
    class Meta:
        model = Profile
        email = Email()
        fields = ('email',)
