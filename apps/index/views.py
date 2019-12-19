from decimal import Decimal
from random import random

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
import time
# 首页

from index.forms import ProductForm
from index.models import OrderInfo
from shopee_shuadan import settings
from shopee_shuadan.settings import UnionPayConfig
from users.models import UserProfile
from utils.alipay import AliPay, get_alipay_url
from utils.email_send import random_str
from utils.pay import UnionPay


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        title = "首页"
        form = ProductForm()
        user = request.user
        return render(request, 'index.html', {'title': title, 'form': form, 'user': user})


class AlipayView(LoginRequiredMixin, View):
    """
    支付宝支付
    get方法实现支付宝return_url，如果没有实现也无所谓，post同样可以更新状态
    post方法实现支付宝notify_url，异步更新

    支付宝返回的url如下：
    #http://127.0.0.1:8000/alipay/return/?
    # charset=utf-8&
    # out_trade_no=201902923423436&
    # method=alipay.trade.page.pay.return&
    # total_amount=1.00&
    # sign=CDBMY9NBsp4KICdQoBEVxGWobd0N8y4%2BU09stzUWwlNtLr7ZpELJdM5js20wXv%2FCPp0FGPbRW1YS9DRx0CnKJULZZMqysBUMH2FL39sS0Fgstgy1ydTs7ySXdHziJV0inI%2BDWAsebQqtjk5gQEweUstc%2B%2BnzjdgAulpvWzfJsbknS%2BqUfktSdF2ZOWGhr1CFlfsMFEDS2nzQv4K3E%2BNaeylkzUnRe9M1sjIL%2FYR0wVZ5A3OfHLPf9HzC2B8%2FLu4g7N5Vctkqp2aerDvIkN5SNmDnRGyjOt2b%2BOsLMqG4X06JSsrZT6Ln8PimsrkSOIGbj0gCqscx7BwZfmCQePlCw%3D%3D&
    # trade_no=2019082622001426981000041778&
    # auth_app_id=2016092600597838&
    # version=1.0&app_id=2016092600597838&
    # sign_type=RSA2&
    # seller_id=2088102177296610&
    # timestamp=2019-08-26+13%3A51%3A01
    """

    def dispatch(self, request, *args, **kwargs):
        self.alipay = AliPay(
            appid=settings.ALIPAY_APPID,
            app_notify_url=settings.ALIPAY_NOTIFY_URL,
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            debug=settings.ALIPAY_DEBUG,
            return_url=settings.ALIPAY_RETURN_URL
        )
        # 处理返回的url参数
        callback_data = {}
        for key, value in request.GET.items():
            callback_data[key] = value
        sign = callback_data.pop('sign', None)
        self.order_sn = callback_data.get('out_trade_no', None)  # 订单号
        self.trade_no = callback_data.get('trade_no', None)  # 支付宝订单号

        # 验证签名
        self.verify = self.alipay.verify(callback_data, sign)
        return super(AlipayView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        """处理支付宝return_url返回"""

        if self.verify:
            self.deposit()
            # 返回个人中心页面
            return redirect(reverse('recharge'))

    def post(self, request):
        """
        处理notify_url
        """
        if self.verify:
            self.deposit()
        return HttpResponse('success')

    def deposit(self):
        """充值操作

        1.更新用户的金币信息
        2.更新订单状态为交易成功
        """

        # 数据库中查询订单记录
        order = OrderInfo.objects.get(order_sn=self.order_sn)
        order.trade_no = self.trade_no  # 支付宝订单号

        # 把人民币转换成对应的金币
        rmb = order.order_mount

        # 更新用户的金币
        order.user.money += Decimal(rmb)
        order.user.save()
        # 订单状态置为交易成功
        order.pay_status = 'TRADE_SUCCESS'
        order.save()


class RechargeView(LoginRequiredMixin, View):
    def get(self, request):
        datetime = time.strftime("%Y-%m-%d", time.localtime())
        return render(request, 'tables.html', {'datetime': datetime})


class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        price = request.POST.get("price", "")
        order_sn = random_str(12)
        while True:
            if OrderInfo.objects.filter(order_sn=order_sn):
                order_sn = random_str(12)
            break

        order_info = OrderInfo()
        order_info.user = request.user
        order_info.order_mount = Decimal(price)
        order_info.order_sn = order_sn
        order_info.save()

        url = get_alipay_url(order_sn, price)
        return redirect(url)


# 获取一个UnionPay对象
def get_uni_object(uid):
    uni_pay = UnionPay(
        version=UnionPayConfig.version,
        mer_id=UnionPayConfig.mer_id,
        front_url=UnionPayConfig.front_url + uid + "/",
        back_url=UnionPayConfig.back_url + uid + "/",
        backend_url=UnionPayConfig.back_url,
        cert_path=UnionPayConfig.cert_path,
        debug=UnionPayConfig.debug,
    )
    return uni_pay


class UnionView(LoginRequiredMixin, View):

    # 生成订单号（自定义）
    # def order_num(self, package_num):
    #     '''
    #     商品代码后两位+下单时间后十二位+用户id后四位+随机数四位
    #     :param package_num: 商品代码
    #     :return: 唯一的订单号
    #     '''
    #     local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    #     result = str(package_num)[-2:] + local_time + str(random.randint(1000, 9999))
    #     return result

    # 账户充值（银联）  # uid参数可不传入，此处用于生成订单号
    def post(self, request, uid):
        price = request.POST.get('price', "")
        unipay_object = get_uni_object(uid)
        order_sn = random_str(8)

        while True:
            if OrderInfo.objects.filter(order_sn=order_sn):
                order_sn = random_str(12)
            break

        order_info = OrderInfo()
        order_info.user = request.user
        order_info.order_mount = Decimal(price)
        order_info.order_sn = order_sn
        order_info.save()

        query_params = unipay_object.build_request_data(
            order_id=order_sn,  # 用户购买订单（每次不一样）
            txn_amt=int(float(price) * 100)  # 交易金额 单位分
        )
        pay_html = unipay_object.pay_html(query_params)
        rsp = HttpResponse()
        rsp.content = pay_html
        # rsp.content = query_params.content
        return rsp


class UnionBackView(View):
    # 充值成功后前台回调(银联)
    def post(self, request, uid):
        if request.method == "POST":
            params = request.POST.dict()
            unipay = get_uni_object(uid)
            res = unipay.verify_sign(params)
            if res:
                if unipay.verify_query(params['orderId'], params['txnTime']):  # 再次查询状态
                    try:
                        user = UserProfile.objects.get(id=uid)
                        user.money += Decimal(float(int(params['txnAmt']) / 100))
                        user.save()
                        return redirect(reverse('recharge'))
                    except UserProfile.DoesNotExist as e:
                        raise e
            else:
                return redirect(reverse('recharge'))


class UnionNotifyView(View):
    # 充值成功后后台回调（银联）
    def post(self, request, uid):
        if request.method == "POST":
            params = request.POST.dict()
            unipay = get_uni_object(uid)
            res = unipay.verify_sign(params)
            if res:
                status = unipay.verify_query(params['orderId'], params['txnTime'])  # 再次查询状态
                if status:
                    try:
                        user = UserProfile.objects.get(id=uid)
                        user.money += Decimal(float(int(params['txnAmt']) / 100))
                        user.save()
                        return HttpResponse('ok')
                    except UserProfile.DoesNotExist as e:
                        raise e
            else:
                return HttpResponse('')
        else:
            params = request.GET.dict()
            for k, v in params.items():
                print(k, v, '\n')
        return HttpResponse('failed')
