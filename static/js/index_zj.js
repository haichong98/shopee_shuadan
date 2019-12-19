$(function (){
    //数量操作
	$(".increment").click(function (){
	    var cc = countItem();
	    if (cc == true){
	       //点击+,操作输入框
            var value = $(this).prev().val();
            //数值自增之后重新赋给输入框显示
            $(this).prev().val(++value);
            countprice();
        }
	});
	$(".decrement").click(function (){
	    var cc = countItem();
	    if (cc == true){
	       if($(this).next().val()>1) {
            //数量大于1才做--
            var value = $(this).next().val();
            $(this).next().val(--value);
            countprice();
        }
        }

	});

	//改变价钱
    $('#shop_price_input').bind('blur',function(){
        var cc = countItem();
	    if (cc == true){
	       countprice();
        }
    });
    $('#select_option1').bind('blur',function(){
        var cc = countItem();
        if (cc == true){
           countprice();
        }
    });
    $('#di3_input_num').bind('blur',function(){
        var cc = countItem();
        if (cc == true){
           countprice();
        }
    });



	//判断商品价钱是否填写正确
    function countItem(){
		var shop_price = $("#shop_price_input").val();
        var f = /[^/d+(/.{1}/d+)?]$/g;
        if (f.test(shop_price)){
            countprice();
            return true
        } else {
            layer.msg("请填写正确商品价钱", {time: 1000});
            return false
        }

	}
    //统计总价钱
    function countprice(){
		var shop_price = $("#shop_price_input").val();
		var di3_input_num = $("#di3_input_num").val();
		var select_option = $("#select_option1").val();
		//套餐一
		if (select_option == 'a'){
		    var countprices = (shop_price*di3_input_num)*(1.25);
            $('.price_count').html("<strong id='price_count'>&yen;"+countprices+"</strong>");
        }
        //套餐二
        else if(select_option == 'b'){
		    var countprices = (shop_price*di3_input_num)*(1.5);
            $('.price_count').html("<strong id='price_count'>&yen;"+countprices+"</strong>");
        }
        //套餐三
        else if(select_option == 'c'){
		    var countprices = (shop_price*di3_input_num)*(2);
            $('.price_count').html("<strong id='price_count'>&yen;"+countprices+"</strong>");
	}
    }

	//提交表单
	$("#di5_submit").click(function () {
        var shop_name = $("#shop_name").val();
        var Key_words_input = $("#Key_words_input").val();
        var shop_id_input = $("#shop_id_input").val();
        var shop_price = $("#shop_price_input").val();
        var select_option = $("#select_option").val();
        var select_option1 = $("#select_option1").val();
        var di3_input_num = $("#di3_input_num").val();
        var textarea = $("#di4text").val();
        var price_count = $("#price_count").html();
        if ($.trim(shop_id_input).length==0) {
            layer.msg("产品ID不能为空", {time: 1000});
            return false;
        }else if ($.trim(Key_words_input).length==0) {
            layer.msg("关键词不能为空", {time: 1000});
            return false;
        }else if ($.trim(shop_price).length==0) {
            layer.msg("产品价格不能为空", {time: 1000});
            return false;
        }
        $.ajax({
            url:'http://127.0.0.1:8000/payment/',
            type:'post',
            data:{'shop_name':shop_name,'Key_words_input':Key_words_input,'shop_id_input':shop_id_input,'shop_price':shop_price,'select_option':select_option,
            'select_option1':select_option1,'di3_input_num':di3_input_num,'textarea':textarea,'price_count':price_count},
            dataType :'json',
            success : function(data){
                if (data.res == 100) {
                    layer.alert('账户余额不足,请及时充值', {icon:1, title:'提示'});
                } else {
                    layer.msg('提交成功', {time: 1000});
                    delete_text();
                }
            },
            error: function (data) {
                layer.msg('请求异常，请刷新页面重试', {time: 1000});
            }
            // 请求成功才开始倒计时
        });


    });



	//取消订单
    $("#di5_button").click(function () {
        delete_text();
    });

    /*清除内容*/
    function delete_text() {
        $("#shop_name").val('');
        $("#Key_words_input").val('');
        $("#shop_id_input").val('');
        $("#shop_price_input").val('');
        $("#select_option").find("option[text='不留星']").attr("selected",true);
        $("#di3_input_num").val('1');
        $("#di4text").val('');
        $('.price_count').html("");
    }

});