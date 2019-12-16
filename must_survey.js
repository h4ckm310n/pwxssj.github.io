var jq = document.createElement('script');
jq.setAttribute('src', 'https://code.jquery.com/jquery-3.4.1.min.js');
document.getElementsByTagName('head')[0].appendChild(jq);

function checkAll() {
	$("input[name^='sq'][value='5']").each(function() {$(this).attr("checked", "checked")});
}
