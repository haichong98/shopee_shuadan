# 登录表单验证
from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'custom_field.html'
    # captcha_1.widget.attrs.update({'placeholder': '验证码'})


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):
    """
    注册验证表单
    """
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # 验证码，字段里面可以自定义错误提示信息
    captcha = CaptchaField(error_messages={'invalid': '验证码'}, widget=CustomCaptchaTextInput)


class ForgetPwdForm(forms.Form):
    """
    忘记密码
    """
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


# 重置密码
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=True, min_length=6,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
