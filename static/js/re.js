	function reply(author, commentid)
	{	
		var commentbox = "comment";
		var cid = commentid.replace('comment-',''); 
		var instr = '[quote id=' + cid + ']' + author.replace(/\n|\t|\r\n/g, "") + '[/quote] \n';
		if (document.getElementById(commentbox) && document.getElementById(commentbox).type == 'textarea') {
			boxid = document.getElementById(commentbox)
		}
		else {
			alert("The comment box does not exist!");
			return 0
		}
		if ( boxid.value.indexOf(instr) > -1 ) {
			alert("你已经添加了这条评论的回复..");
			return 0
		}
		if (boxid.value.replace(/\s|\t|\n/g, "") == '') {
			boxid.value = instr
		}
		else {
			boxid.value = boxid.value.replace(/[\n]*$/g, "") + '\n\n' + instr;
		}
	}

    function cumulativeOffset(e) {
        var top = 0,
        left = 0;
        do {
            top += e.offsetTop || 0;
            left += e.offsetLeft || 0;
            e = e.offsetParent
        } while ( e );
        return [left, top]
    };
	
jQuery(document).ready(function(){

		var id = /^#comment-/;
		var at = /^@/;
		var commentlist = jQuery('.comment-list');
		commentlist.find('li p a').each(function() {
			if (jQuery(this).attr('href').match(id) && jQuery(this).text().match(at)) {
				jQuery(this).addClass('atreply')
			}
		});
		jQuery('.atreply').hover(function() {
			var atreply = this;
			var atreplyself=jQuery(atreply);
			var offset = atreplyself.offset();
			var commentid = jQuery(this).attr('href');
			jQuery('<li class="tip"></li>').hide().html('<div class="arrow"></div><div class="innerbox">' + jQuery(commentid).html() + '</div>').appendTo(jQuery('.comment-list'));
			commentlist.find('.tip').css({left: atreplyself.width() + 20,top: offset.top - 60}).fadeIn(200)
		},
		function() {
			commentlist.find('.tip').fadeOut(200,
			function() {
				jQuery(this).remove()
			})
		})

});