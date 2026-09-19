from django import forms
from .models import Tweet
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control tweet-textarea',
                'placeholder': "What is happening?!",
                'rows': 3,
                'maxlength': 240,
                'id': 'tweet-input-text',
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control tweet-file-input visually-hidden',
                'id': 'tweet-input-photo',
                'accept': 'image/*',
            }),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control custom-input',
            'placeholder': 'name@example.com',
            'autocomplete': 'email',
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Choose a username',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control custom-input',
                'placeholder': 'Create password',
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control custom-input',
                'placeholder': 'Confirm password',
            })
