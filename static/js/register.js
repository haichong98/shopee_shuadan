$(function (){
    var code = "邮箱验证";
    //点击提交时,检测表单数据是否正确
    $('form').submit(function() {
        var username = $("#username").val();
        var atpos=username.indexOf("@");
	    var dotpos=username.lastIndexOf(".");
	    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=username.length){
	        layer.msg("不是一个有效的 e-mail 地址", {time: 1000});
	        return false;
	    }
	    var password = $("#password").val();
        var re_n = /[^\d]/g;
        var re_t = /[^a-zA-Z]/g;
        if ($.trim($("#password").val()).length==0) {
            layer.msg("不能为空码", {time: 1000});
            return false;
        } else if (password.length < 6 || password.length > 16) {
            layer.msg("长度应为6-16个字符", {time: 1000});
            return false;
        } else if (!re_n.test(password)) {
           layer.msg("不能全部为数字", {time: 1000});
            return false;
        } else if (!re_t.test(password)) {
            layer.msg("不能全部为字母", {time: 1000});
            return false;
        }
        var repassword = $("#repassword").val();
        if (repassword != password) {
            layer.msg("两次输入不一致", {time: 1000});
            return false;
        }
        var codes = $("#code").val();
        if (codes != code || codes == '邮箱验证'){
            layer.msg("验证码不正确", {time: 1000});
            return false;
        }
    });

    //当邮箱输入框失去焦点时
    $('#username').bind('blur',function(){
        //获取username 的值,判断是否为正确有效
        var username =$("#username").val();
        var atpos=username.indexOf("@");
	    var dotpos=username.lastIndexOf(".");
	    if (atpos<1 || dotpos<atpos+2 || dotpos+2>=username.length){
	        layer.msg("不是一个有效的 e-mail 地址", {time: 1000});
	        var name = 0
	    }});

    //查看服务条款
    $('#fuwu').bind('click', function(){
        layer.open({
          type: 1,
          title: false, //不显示标题栏
          btn: ['我已完整阅读，并承诺遵守'],
          area: ['600px', '360px'],
          closeBtn: false,
          shade: 0.8,
          resize: false,
          content: '\<\div style="padding:20px;">不得通过本站提供的服务发布、转载、传送含有下列内容之一的信息：<br>1.违反宪法确定的基本原则的；<br>2.危害国家安全，泄漏国家机密，颠覆国家政权，破坏国家统一的；<br>3.损害国家荣誉和利益的；<br>4.煽动民族仇恨、民族歧视，破坏民族团结的；<br>5.破坏国家宗教政策，宣扬邪教和封建迷信的； <br>6.散布谣言，扰乱社会秩序，破坏社会稳定的；<br>7.散布淫秽、色情、赌博、暴力、恐怖或者教唆犯罪的；<br>8.侮辱或者诽谤他人，侵害他人合法权益的；<br>9.煽动非法集会、结社、游行、示威、聚众扰乱社会秩序的；<br>10.以非法民间组织名义活动的；<br>11.含有法律、行政法规禁止的其他内容的。\<\/div>'
        });
    });

    //发送验证码
    $('#sendCode').bind('click',function(){
        var flag = true;
        var username = $("#username").val();
            if (username == '' || username == undefined) {
                layer.msg("请填入邮箱", {time: 1000});
                return false;
            }
            $.ajax({
                url:'http://127.0.0.1:8000/sendCode/',
                type:'post',
                data:{'username':username},
                dataType :'json',
                success : function(data){
                    code = data.code;
                    if (data.res != 200) {
                        layer.msg(data.res, {time: 1000});
                        $("#sendCode").attr('disabled', false);
                        flag = false;
                    } else {
                        layer.alert('验证码已发送至您的邮箱，请稍作等待或查看垃圾箱', {icon:1, title:'提示'});
                        $("#sendCode").attr('disabled', true);
                        flag = true;
                    }
                },
                error: function (data) {
                    layer.msg('请求异常，请刷新页面重试', {time: 1000});
                    flag = false;
                }
                // 请求成功才开始倒计时
            });
            if (flag) {
                // 60秒后重新发送
                var left_time = 60;
                var tt = window.setInterval(function () {
                    left_time = left_time - 1;
                    if (left_time <= 0) {
                        window.clearInterval(tt);
                        $("#sendCode").attr('disabled', false).val('发送');
                    } else {
                        $("#sendCode").val(left_time);
                    }
                }, 1000);
            }

    });
});
