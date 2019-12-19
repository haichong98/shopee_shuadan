from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse
from django.views.generic.base import View

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from utils.email_send import send_register_email
from .models import UserProfile, EmailVerifyRecord


# 邮箱和用户名都可以登录
# 基础ModelBackend类，因为它有authenticate方法


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户登出
class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, '登出成功')
        return HttpResponseRedirect(reverse('login'))


# 用户登录
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))

        title = "登录"
        login_form = LoginForm()
        return render(request, 'login.html', {'title': title, 'login_form': login_form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        title = "登录"
        # 获取用户提交的用户名和密码
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    # 只有注册激活后才能登陆
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, '登录成功', extra_tags='success')
                    return redirect(reverse('index'))
                else:
                    messages.add_message(request, messages.ERROR, '用户未激活', extra_tags='danger')
                    return render(request, 'login.html', {'form': login_form})
            else:
                messages.add_message(request, messages.ERROR, '用户名或密码错误', extra_tags='danger')
                return render(request, 'login.html', {'form': login_form})
        # form.is_valid（）已经判断不合法了，所以这里不需要再返回错误信息到前端了
        else:
            danger = 50
            messages.add_message(request, messages.ERROR, "用户名或密码错误", extra_tags='danger')
            return render(request, 'login.html', {'title': title, 'form': login_form})


# 用户注册
class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        register_form = RegisterForm()
        return render(request, 'sign-up.html', {'register_form': register_form, 'title': '注册'})

    def post(self, request):
        title = "注册"
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            # 如果用户已存在，则提示错误信息
            if UserProfile.objects.filter(email=email):
                messages.add_message(request, messages.WARNING, '用户已存在', extra_tags='warning')
                return render(request, 'sign-up.html', {'register_form': register_form, 'title': title})

            password1 = request.POST.get('password1', None)
            password2 = request.POST.get('password2', None)
            if password1 != password2:
                messages.add_message(request, messages.ERROR, '密码不一致！', extra_tags='danger')
                return render(request, 'sign-up.html', {'register_form': register_form, 'title': title})
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = email
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.password = make_password(password2)
            user_profile.save()
            send_register_email(email, 'register')
            messages.add_message(request, messages.SUCCESS, '邮件已发送，请查收')
            return redirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR, '注册失败，请重新注册', extra_tags='danger')
            return render(request, 'sign-up.html', {'register_form': register_form, 'title': title})


# 用户激活
class ActiveUserView(View):
    def get(self, request, active_code):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))

        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            messages.add_message(request, messages.ERROR, '激活失败', extra_tags="danger")
            return render(request, 'active_fail.html')
        # 激活成功跳转到登录页面
        messages.add_message(request, messages.SUCCESS, '激活成功')
        return redirect(reverse('login'))


# 找回密码
class ForgetPwdView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'title': "忘记密码"})

    def post(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_email(email, 'forget')
            messages.add_message(request, messages.SUCCESS, '邮件已发送，请查收')
            return redirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR, '表单验证失败，请重新提交表单', extra_tags="danger")
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# 重新激活
class ReActiveView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        forget_form = ForgetPwdForm()
        return render(request, 'reactive.html', {'forget_form': forget_form, 'title': "忘记密码"})

    def post(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            user = UserProfile.objects.get(email=email)
            if user.is_active:
                messages.add_message(request, messages.WARNING, '用户已激活，请勿重复激活', extra_tags="warning")
                return redirect(reverse('login'))
            send_register_email(email, 'reactive')
            messages.add_message(request, messages.SUCCESS, '邮件已发送，请查收')
            return redirect(reverse('login'))
        else:
            messages.add_message(request, messages.ERROR, '表单验证失败，请重新提交表单', extra_tags="danger")
            return render(request, 'reactive.html', {'forget_form': forget_form})


# 重新设置密码
class ResetView(View):
    def get(self, request, active_code):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {"email": email})
        else:
            messages.add_message(request, messages.ERROR, '邮箱验证失败', extra_tags="danger")
            return redirect(reverse('forget_pwd'))


# 验证密码
class ModifyPwdView(View):
    def post(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.INFO, '用户已登录，请登出后再访问')
            return redirect(reverse('index'))
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                messages.add_message(request, messages.ERROR, '密码不一致！', extra_tags="danger")
                return render(request, "password_reset.html", {"email": email})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            messages.add_message(request, messages.SUCCESS, '设置成功')
            return redirect(reverse('login'))
        else:
            email = request.POST.get("email", "")
            messages.add_message(request, messages.ERROR, '表单验证失败，请重新提交表单', extra_tags="danger")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 用户中心
class UserView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        title = '用户中心'
        return render(request, "user_info.html", {"title": title, "user": user})
