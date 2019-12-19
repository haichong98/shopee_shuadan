$(function () {
    $('#tiao_button').bind('click', function () {
        var t = $("#tiao_num").val();//这个就是我们要判断的值了
        if (!isNaN(t)) {
            var url = 'http://127.0.0.1:8000/Bill/?page='+t;
            $(location).attr('href',url);

        } else {
            layer.msg("请输入正确页码", {time: 1000});
        }
    });
    //当前页数
    var current_page = $("#current").html();
    current_page=Number(current_page);
    //一共有多少页
    var presence_page = $('.presence').length;
    presence_page=Number(presence_page);
    if (presence_page<=5){
        //页码数小于5
        var d=$('.presence').slice(0,presence_page);
        $.each(d,function (index,ele){
        $(ele).css('display','inline-table');
        });
    }else {
        //页码数大于5
        if(current_page+2 > presence_page){
            //末尾五页
            var d1=$('.presence').slice(presence_page-5,presence_page);
            $.each(d1,function (index,ele){
            $(ele).css('display','inline-table');
            });
        }else if(current_page<=3) {
            //首五页
            var d2=$('.presence').slice(0,5);
            $.each(d2,function (index,ele){
            $(ele).css('display','inline-table');
            });
        }else {
            //中间五页
            var d3=$('.presence').slice(current_page-3,current_page+2);
            $.each(d3,function (index,ele){
            $(ele).css('display','inline-table');
            });
        }

    }

});