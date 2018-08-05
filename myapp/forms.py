from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django import forms

from .models import File

class LoginForm(forms.Form):
    username = forms.CharField(
            label='用户名',
            min_length=3, 
            max_length=20,
            widget=forms.TextInput(attrs={'class': 'input'}),
        )
    password = forms.CharField(
            label='密  码',
            min_length=8,
            max_length=20,
            widget=forms.PasswordInput(attrs={'class': 'input'}),
        )

    captcha = forms.CharField(
            label='验证码',
            min_length=4,
            max_length=4,
            widget=forms.TextInput(attrs={'class': 'input'}),
        )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
            return username
        except User.DoesNotExist: # 不检查存在多个结果的情况，注册那里就不允许重复用户名
            raise ValidationError('抱歉，该用户名并不存在')


class SignupForm(UserCreationForm):
    password1 = forms.CharField(
        label="密 码",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        # help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(attrs={'class': 'input'}),
        strip=False,
        # help_text=_("Enter the same password as before, for verification."),
    )    
    username = forms.CharField(
        label='用户名',
        min_length = 4,
        max_length = 12,
        widget=forms.TextInput(attrs={'class': 'input'}),
    )
    def clean_username(self):
        ALLOWD_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'
        username = self.cleaned_data['username']
        if len(username) < 4 or len(username) > 12:
            raise ValidationError('您的用户名必须是 4 到 12 个字符，且只能包含英语字母，下划线或者数字')
        if not all([char in ALLOWD_CHARS for char in username]):
            raise ValidationError('您的用户名必须是 4 到 12 个字符，且只能包含英语字母，下划线或者数字')
        if User.objects.filter(username=username):
            raise ValidationError('抱歉，该用户名已经被注册')
        else:
            return username


class UploadForm(forms.Form):
    files = forms.FileField(
        label='',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )


class CreateDirectoryForm(forms.Form):
    """
        创建目录，和 mkdir view函数绑定
        todo: 添加具体的 clean 规则
        和 unix 系统的目录命名规则一致
    """
    name = forms.CharField(
        label='目录名 ',
        widget=forms.TextInput(attrs={'class': 'input'}),
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if '/' in name or '%' in name:
            raise ValidationError('抱歉，目录名不可以包含 "/" 或 "%"')
        else:
            return name.strip()


class EditForm(forms.Form):
    """
        编辑文件信息，
        todo 编辑文件信息
    """       
    name = forms.CharField(
        label='文件名',
        widget=forms.TextInput(attrs = {'class': 'input'}),
    )
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if '/' in name or '%' in name:
            raise ValidationError('抱歉，文件名不可以包含 "/" 或 "%"')
        else:
            return name.strip()    











