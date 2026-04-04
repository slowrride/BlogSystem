from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    自定义用户注册表单
    """
    email = forms.EmailField(required=True, label='邮箱')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """
    用户资料编辑表单
    """
    class Meta:
        model = User
        fields = ('avatar', 'bio', 'email')
        labels = {
            'avatar': '头像',
            'bio': '个人简介',
            'email': '邮箱',
        }
