from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    nick_name = models.CharField('昵称', max_length=50, default='')
    mobile = models.CharField('手机号', max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField('邮箱', unique=True, max_length=100, null=True, blank=True)
    money = models.DecimalField('账号余额', max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField('头像', upload_to='image/touxiang', default='image/touxiang/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码')
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField('验证类型', choices=send_choices, max_length=10)
    send_time = models.DateTimeField('发送时间', default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
