from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import Operator


class OperatorCreationForm(UserCreationForm):
    class Meta:
        model = Operator
        fields = ('username', 'first_name', 'last_name', 'second_name', 'password1', 'password2', 'is_superuser')


class OperatorChangeForm(forms.ModelForm):
    class Meta:
        model = Operator
        fields = ('username', 'first_name', 'last_name', 'second_name', 'is_superuser')


class OperatorPasswordResetForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")

    class Meta:
        model = Operator
        fields = []