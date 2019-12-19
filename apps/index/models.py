from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
class Product(models.Model):
    product_title = models.CharField('产品标题', max_length=50, default='')
    product_price = models.FloatField('产品价格')
    number = models.IntegerField('刷单数量')
    brush_price = models.FloatField('刷单价格')
    key_word = models.CharField('关键词', max_length=50, default='', null=True, blank=True)

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_title

# 充值订单详情
@python_2_unicode_compatible
class OrderInfo(models.Model):
    ORDER_STATUS = (
        ('TRADE_SUCCESS', '交易支付成功'),
        ('TRADE_CLOSED', '未付款交易超时关闭'),
        ('WAIT_BUYER_PAY', '交易创建'),
        ('TRADE_FINISHED', '交易结束'),
        ('paying', '待支付'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    order_sn = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name='订单号')
    trade_no = models.CharField(max_length=100, unique=True, null=True, blank=True, verbose_name='支付订单号')

    pay_status = models.CharField(choices=ORDER_STATUS, max_length=40, verbose_name='订单状态', default='paying')
    order_mount = models.DecimalField(verbose_name="充值金额", max_digits=10,
                                      decimal_places=2, default=0.00)

    class Meta:
        verbose_name = "充值订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn
