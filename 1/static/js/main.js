// init
$(function ($) {
    choiceCode();
    addTheme();
    UploadBlog();
})


// 添加分类
function addType(){
    var name = $('#msTitle').val().trim();
    if(! name){
        return $('#ms_title').show();
    }else{
        $.post('/manage/add_type/', {'name': name}, function(data){
            var r = data.evalJson();
            if(r.response == 'ok'){
                $('#s_ms_box').hide();
                $('#sendok').show();
                $('#adds').before('<button type="button" class="btn btn-default" style="margin-right: 10px;display: block" id="c_'+ r.data+'">'+name+'</button>')
                $('#c_'+ r.data).bind('click',choiceCode())
            }else{
                return $('#ms_title').text('系统出差').show();
            }
        })
    }
}


// 选择方向效果
function choiceCode(){
    $('#codes button').click(function(){
        $('#codes button').attr('class','btn btn-default');
        $(this).addClass('btn btn-success');
    })
}


//添加标签
function addIt(elem){
    var tags = getTags();
    var title = $.trim(elem);
    if(jQuery.inArray( title, tags ) == -1){
        $('.bootstrap-tagsinput input').before('<span class="tag label label-info">'+title+'<span data-role="remove"></span></span>')
    }
    $('span[data-role="remove"]').bind('click',function(){
        $(this).parent().remove();
    })
}
//获取标签
function getTags(){
    var tags = new Array()
    $('.bootstrap-tagsinput span').each(function(){
        tags.push($(this).text())
    })
    return tags
}



//发布
function addTheme(){
    $('#submit').click(function(){
        var code = $('#codes').find('button.btn.btn-default.btn-success');
        if(!code.length){
            return alert('选择类型')
        }
        var code = code.attr('id').split('_')[1];
        $('input[name="type"]').val(code);
        //　获取标签转换成字符串
        var tags = getTags();
        tags = JSON.stringify(tags);
        $('input[name="id_tag"]').val(tags);
        var title = $.trim($('#id_title').val());
        var pwd = $.trim($('#id_is_show').val());
        if(!title){
            return alert('填写标题了');
        }

        setBtn('off',$('#submit'),'发布笔记');     //禁用按钮
        $("#themeform").submit();   // 表单提交
    })
}


//发布上传
function UploadBlog(){
    $('#upload').click(function(){
        var code = $('#codes').find('button.btn.btn-default.btn-success');
        if(!code.length){
            return alert('选择类型')
        }
        var code = code.attr('id').split('_')[1];
        $('input[name="type"]').val(code);
        //　获取标签转换成字符串
        var tags = getTags();
        tags = JSON.stringify(tags);
        $('input[name="id_tag"]').val(tags);
        blog = $('#blog').val();
        setBtn('off',$('#submit'),'发布笔记');     //禁用按钮
        $("#uploadform").submit();   // 表单提交

    })
}