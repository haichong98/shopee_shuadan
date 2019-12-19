"""
Django settings for shopee_shuadan project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#x@@wc_%v70)l4=74oq1+3waxtn4p79n%1h59ig8_6)hu(_fz2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'users.UserProfile'
# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.forms',
    'users',
    'xadmin',
    'crispy_forms',
    'bootstrap3',
    'captcha',
    'index'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shopee_shuadan.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        # 'DIRS': []
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'shopee_shuadan.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopeeshuadan',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

EMAIL_HOST = "smtp.qq.com"  # SMTP服务器主机
EMAIL_PORT = 25  # 端口
EMAIL_HOST_USER = "1243726062@qq.com"  # 邮箱地址
EMAIL_HOST_PASSWORD = "dlpewwqowwcjhaja"  # 密码
EMAIL_USE_TLS = True
EMAIL_FROM = "1243726062@qq.com"  # 邮箱地

LOGIN_URL = "/login/"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 支付宝测试
ALLOWED_HOSTS = ['*']
# APPID
ALIPAY_APPID = "2016101600699292"  # 沙箱APPID，生产环境须更改为应用APPID。
ALIPAY_DEBUG = True
# 网关
ALIPAY_URL = "https://openapi.alipaydev.com/gateway.do" # 沙箱网关，生产环境须更改为正式网关。
# ALIPAY_URL = "https://openapi.alipay.com/gateway.do" # 正式网关，开发环境勿使用。

# 回调通知地址
# ALIPAY_NOTIFY_URL = "http://127.0.0.1:8888/pay_result/" # 如果只可以内网访问开发服务器
ALIPAY_NOTIFY_URL = "http://127.0.0.1:8000/alipay/return/"  # 如果生产环境或外网可以访问开发服务器
ALIPAY_RETURN_URL = "http://127.0.0.1:8000/alipay/return/"  # return_url可以单独设置，本文中保持一致。

# 使用密钥文件
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'apps/index/keys/private_2048.txt')
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'apps/index/keys/alipay_key_2048.txt')

# 使用密钥字符串
APP_PRIVATE_KEY = 'MIIEowIBAAKCAQEAzeuYwPbgbFORReiKv3GogU9NvPMv5hhacZDJWIJulwAfk21AZqMB4raC1zIv1JTrZNUyDIzV198/DK6zZcJ7yUtR9gdo7ItekT787tT6Vs84Pc9+boFBk83GPottkJ4lDqTzLr1L3W0Cxni/MRfTMi1PcVn4zSZ7d5nFzlUbF/muX5vkvKUQTwPvZJNCHzOqN69j1MUiYJ6rzqCBiOil8nZ3vbz32l3du3UPuTUqHHNP8jDEm+xpj68DN2UUiseDZjeeO9oHogNe1DSk2ktOCJEu4idk+HHbGaUMQnNM7bKUC7qzeptpOwM+4h4g4H2wo8RL1aa5dNAHLYCHz/TFawIDAQABAoIBAGvio4V10t7uaY5W51qmEcKt6ey0/MNwvvIBCXx12bsDNYfoFXWwsaw2MxbMFIMsAqgxiqdIokEXldDvNs55tqEf9TERcMd9vW4bsijvLLmOl8jKjVMYJWNqzBK4ug6qzH9/rGkwhC7ejjWtzX3LHbuMQbMBkHjrUIS47AnOTQOhux5N/KjPNg8sW0SUiytB4o6ysIB3djnTYowWyYQaUqTWjoJ/NwLem97R4kCU3OQf0nkYwAKNSaERcAxsd53WF6LhIS1fmUT+HL8nCDy6bY3lgEHGnm1IGxYAjcyJe0mTzs0jJqRHbQXDI5pCojDz//C/uy/9Y/6XMKZn1MASAQECgYEA/ScUCpGEe2uqMmYvlUoF8VjNVf6JoFcpyiTfsgdGQab7O6xubsu6p77S7Dw4lrkqkp2EilKkr/3B0LXQ3vPX9w3V1ocIntLgQg5XnDq7wIUUW1eQR354Fyb01/kyCsQ66FrwVz7vJtDsBRkeMjrJOkJJJy+ZoJ9whO/vIqFiwU0CgYEA0DyEycZbSBOGwK9M5GyU7P8sBVf2Y16PJxhEWPfxbo9ouC7J7nCIvM4+4UNQ0IR4w9NG4ZF4yEFSd7YX4JO7YH+QRgwiPVpLqJppvig/yg0/KpHvY7XPtlzj8tES6jifzzuDHW4lztd64j6TKiWopVin6GiNTk5e6v8detWHRZcCgYEAkUwPna09u9Tkv76UyvvMg2RznkrU1RmSG7qkRbsVIPNlOS/TxnXaMRM+XmaGGEQ44iPUgcvDSFu+FTt1obGVH/Bp7pJcaUQhgOhYcovnXS1ErNSKM+6roKY0W41kondUVC51ya2Od9nrzVVIVo4VFwIamIoig+VfIH3R5C96zfUCgYAbxtbXq3Plq2UgMsII/krnSipvFAqzuptR1bTYQUqdOtf3KZaaDbzPoptUpQwUpHcPeBFOaX85By2e9lU9CbfG6X0vOtMeZ/sLpH1Sdj/8DcRNQ2YxYMEyTDXD4Aur3p3CoOeed2DntGqZ30r2JkvWsnrDT575wQ58PkeKaQ1ARQKBgELU1V+VSL6nqsSrrb+wDHazqSfd0DKph0XEcv9FgAQV4tMEoFQKVeryKY+sk7tRHVz0p0BDlBLpcuDmWl/ZVNurXYt/2WPPHhGhG4Qe+3ETmQDUZv/+bZGa8SatXuRLbied4ybqgphlqO3AWr5hGCF5yDt4ibtdnm+A/SgXK69J' # 应用私钥
ALIPAY_PUBLIC_KEY = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvEa8ljsryD5gR6/iFR4MvQIMRrW2k2IDe7gH/vPD8I8kKp4urI0L2udkzHFXdWr/I11kM/F44Ve57GIX7j0NSNbsqbLvOtBPNoE08GSXgWGLZpGiklHDaj+Q67wC9JnmTkf7t3FbbDAbJdd/upUGJ0rD5xOvdBhaWaJIM4w0U53Y/knXztIDH69J1BTmT8V49u5nIP3AJJRtF6ERNQDeJB0bj4rb3Ak03PrptnvVht8fVY3X7XTEZBjSptSFbHqkdnlzDAnZ//WmOvqL6cik/sQTRunysZ+XSyCYI8Q//ziHzVxeBfR2sdlml8CjO3DU0nzaeEJQ83TIc+cwAHOKGQIDAQAB' # 支付宝公钥


# 银联测试
# 银联支付参数配置
class UnionPayConfig(object):

    # 银联版本号(固定)
    version = "5.1.0"

    # 商户ID(配置项)
    mer_id = "777290058175192"  # 你的商户id  （正式生产环境需修改）

    # 前台回调地址(支付成功回调成功)(配置项)（正式生产环境需修改）
    front_url = "http://127.0.0.1:8000/uni_back/"  # http://公网IP/back/

    # 后台回调地址(配置项)（正式生产环境需修改）
    back_url = "http://127.0.0.1:8000/uni_notify/"  # http://公网IP/notify/

    # 证书地址(配置项)（正式生产环境需修改）
    cert_path = os.path.join(BASE_DIR, 'apps/index/keys/acp_test_sign.pfx')

    # 证书解密密码(根据实际去调配)(配置项) （正式生产环境需修改）
    cert_password = "000000"

    # 是否开启测试模式(默认False)(配置项)（正式生产环境为False）
    debug = True