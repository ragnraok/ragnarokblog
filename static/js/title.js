jQuery(document).ready(function() {
	jQuery("#main>.post>.title>h2>a").live("click",
	function() {
		var t = "努力载入中",
		r = jQuery(this).html(t).unbind("click"),
		u = 5;
		m();
		window.location = $(this).attr("href");
		function m() { (u < 0) ? (u = 5, r.html(t), m()) : (r[0].innerHTML += ".", u--, setTimeout(m, 200))
		}
	});
});