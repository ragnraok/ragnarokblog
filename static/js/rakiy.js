//页面载入调用
jQuery(document).ready(function (){
	ArtLoading(),
	ImgChange()
});





//新窗口打开
jQuery(document).ready(function(){
	jQuery("a[rel='external'],a[rel='external nofollow']").click(
	function(){window.open(this.href);return false})
});
//订阅图标转换
jQuery(document).ready(function(jQuery){
			jQuery('.icon1,.icon2,.icon3,.icon4,').wrapInner('<span class="hover"></span>').css('textIndent','0').each(function () {
				jQuery('span.hover').css('opacity', 0).hover(function () {
					jQuery(this).stop().fadeTo(350, 1);
				}, function () {
					jQuery(this).stop().fadeTo(350, 0);
				});
			});
});
//延迟加载
jQuery(document).ready(function() {          
    	jQuery(".content img").not("#response img").lazyload({
        	placeholder:"http://85s.me/t/usr/themes/Z01/images/img_load.gif",
            effect:"fadeIn"
        });
});
// 滚屏
jQuery(document).ready(function(){
jQuery('#roll_top').click(function(){jQuery('html,body').animate({scrollTop: '0px'}, 800);}); 
});

//页面载入
function ArtLoading(){
	jQuery('article h2 a').click(function(){
		var i = 6;
		var l = jQuery(this);
		l.text('Loading');	
		dot();
		window.location = jQuery(this).attr('href');
		function dot(){
			if (i < 0){ 
				i = 6;
				l.text('Loading');	
				dot();
			}else{
				l[0].innerHTML += '.';	
				i--;
				setTimeout(dot, 400);
			}
		}	
	});
}

//图片渐显
function ImgChange(){
	jQuery('img').hover(
		function() {jQuery(this).fadeTo("fast", 0.5);},
		function() {jQuery(this).fadeTo("fast", 1);
	});
}