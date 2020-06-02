from allauth.account.signals import email_confirmed
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Reviews, Profile


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ("name", "text")


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Введите действительный адрес электронной почты.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




class SendEmailForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea)
    users = forms.ModelMultipleChoiceField(label="To", queryset=User.objects.all(), widget=forms.SelectMultiple())


class SetPasswordForm(forms.Form):
    user = forms.CharField(widget=forms.HiddenInput)
    current_password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'Текущий пароль'
    }))

    new_password1 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'Новый пароль'
    }))

    new_password2 = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'type': 'password',
        'placeholder': 'Подтвердить новый пароль'
    }))

    def clean(self):
        username = self.cleaned_data['user']
        current_password = self.cleaned_data['current_password']
        new_password1 = self.cleaned_data['new_password1']
        new_password2 = self.cleaned_data['new_password2']

        user = authenticate(username=username, password=current_password)

        if not user:
            msg = 'Неправильный текущий пароль'
            self._errors['current_password'] = self.error_class([msg])
            self.cleaned_data.pop('current_password')

        elif new_password1 != new_password2:
            msg = 'Пароли не совпадают'
            self._errors['new_password2'] = self.error_class([msg])
            self.cleaned_data.pop('new_password1')
            self.cleaned_data.pop('new_password2')


        return self.cleaned_data