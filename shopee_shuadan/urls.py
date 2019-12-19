"""shopee_shuadan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve

import xadmin
from index.views import IndexView, RechargeView, OrderView, AlipayView, UnionView, UnionBackView, UnionNotifyView
from users.views import LoginView, RegisterView, LogoutView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, \
    ReActiveView
from .settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    # user
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name='register'),
    path('captcha/', include('captcha.urls')),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    re_path('reactive/', ReActiveView.as_view(), name='reactive'),
    # path('user/', UserView.as_view(), name='user'),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # index
    path('', IndexView.as_view(), name='index'),
    # recharge
    path('recharge/', RechargeView.as_view(), name='recharge'),
    path('order/', OrderView.as_view(), name='order'),

    # 支付宝支付
    path('alipay/return/', AlipayView.as_view(), name='Ali'),

    # 银联支付
    path('unipay/<str:uid>/', UnionView.as_view(), name='unipay'),
    path('uni_notify/<str:uid>/', UnionNotifyView.as_view(), name='uni_notify'),
    path('uni_back/<str:uid>/', UnionBackView.as_view(), name='uni_back')

]
