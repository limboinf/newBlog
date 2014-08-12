/**
 * Created by beginman on 14-8-11.
 */
function markIt(id, type){
    var url = '/english/ok/';
    $.post(url, {'id':id, 'type':type}, function(data){
        if(data == 'ok'){
            location.reload();
        }else{
            alert('系统异常');
        }
    })
}