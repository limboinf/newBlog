$(function($){
    webnav();   // top nav
    CommonDel();    // common delete.
    MyPicEdit();
})

//按钮禁用与激活
function setBtn(type, obj,txt){
    if(type == 'off'){
        obj.text('正在处理中……');
        obj.attr('disabled','disabled')
    }else{
        obj.text(txt);
        obj.removeAttr('disabled');
    }
}

//导航
function webnav(){
    var path = window.location.pathname;
    if(path.indexOf('wiki') > -1){
        $('#webnav li').removeClass();
        $('#wiki').addClass('active');
    };
    if(path.indexOf('pic') > -1){
        $('#webnav li').removeClass();
        $('#pic').addClass('active');
    };
    if(path.indexOf('about') > -1){
        $('#webnav li').removeClass();
        $('#about').addClass('active');
    }
    if(path.indexOf('resume') > -1){
        $('#webnav li').removeClass();
        $('#resume').addClass('active');
    }
    if(path.indexOf('english') > -1){
        $('#webnav li').removeClass();
        $('#english').addClass('active');
    }
}


// 获取url参数
(function($){
    $.getUrlParam = function(name)
    {
        var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
        var r = window.location.search.substr(1).match(reg);
        if (r!=null) return unescape(r[2]); return null;
    }
})(jQuery);

// 删除
function delBlog(id){
    if(confirm('是否确定删除？')){
        var url = '/manage/blog/del/';
        $.post(url, {"id": id}, function(data){
            if(data == 'ok'){
                location.reload();
            }else{
                alert('系统出错');
            }
        })
    }
}

/** trim() method for String */
String.prototype.trim=function() {
	return this.replace(/(^\s*)|(\s*$)/g,'');
};


// common del
function CommonDel(){
    $('.pic_type_del').click(function(){confirm('是否删除') ? commonPost('pictype', $(this)):null});    // 删除picType
    $('#picdel').click(function(){confirm('是否删除') ? commonPost('pic', $(this)):null});              // 删除pic
    $('.mypicdel').click(function(){confirm('是否删除') ? commonPost('mypic', $(this)):null});          // 删除mypic

    function commonPost(model, elem){
        var url = '/common/del/';
        id = elem.attr('type');
        $.post(url, {'model':model,'id':id}, function(data){
           data == 'ok' ? location.reload() : alert('删除失败');
        })
    }
}

// edit mypic
function MyPicEdit(){
    $('.mypic_edit').click(function(){
       $(this).siblings('textarea').show(300);
       $(this).html('<span class="picedit"><span class="glyphicon glyphicon-check"></span>&nbsp保存</span>');
       var that = $(this);
        $('.picedit').bind('click', function(){
            picedit(that);
        })
    })
}

function picedit(elem){
   var txt = elem.siblings('textarea').val();
   var id = elem.attr('type');
   var url = '/manage/pic/edit_mypic/';
   $.post(url, {'desc': txt, 'id':id}, function(data){
       data == 'ok' ? location.reload() : alert('操作失败');
   })
}