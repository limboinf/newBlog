/**
 * Created by beginman on 14-8-8.
 */
	function getFlashObject_top(movieName) {
	if (window.document[movieName]) {
		return window.document[movieName];
	}
	if (navigator.appName.indexOf("Microsoft Internet")==-1) {
		if (document.embeds && document.embeds[movieName])
		return document.embeds[movieName];
	} else  {
		return document.getElementById(movieName);
	}
}
function dispCofirm(){
	var confirmflag = confirm("您没有安装flash播放插件，所以无法发音，请先安装下吧！");
	if(confirmflag){
		var url = 'http://www.adobe.com/go/getflashplayer';
		var wo = window.open();
		setTimeout(function(){if(wo)wo.location = url;}, 50);
	}
}

var old = null;//存储前一次发音对象
function asplay_top(c){
	var audio = document.createElement("audio");
	if(audio != null && audio.canPlayType && audio.canPlayType("audio/mpeg")){
		if(old){
			old.pause();//如果多次触发发音，则先停止上一次的发音
		}
		audio.src = c;
		old = audio;
		audio.play();
	}else{
		var asound = getFlashObject_top("news_iciba");
		if(asound){
			try{
				asound.SetVariable("f",c);
				asound.GotoFrame(1);
			}catch(e){
				dispCofirm();
			}
		}
	}
}
function asstop_top(){
	var asound = getFlashObject_top("asound_top");
	if(asound){
		asound.GotoFrame(3);
	}
}
var timer = null;
function  iciba_common_top_callback(mp3) {
	asplay_top(mp3);
}
function  iciba_common_top_onSecondDelay(mp3) {
	clearTimeout(timer);
//	var mp3_1 = "iciba_common_top_callback('"+mp3+"')";
//	timer = setTimeout(mp3_1, 100);
	timer = setTimeout(function(){iciba_common_top_callback(mp3); return false;}, 100);
}
