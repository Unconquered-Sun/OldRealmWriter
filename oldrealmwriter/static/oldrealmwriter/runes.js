$(document).ready(function(){
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			var cookies = document.cookie.split(';');
			for (var i = 0; i < cookies.length; i++) {
				var cookie = jQuery.trim(cookies[i]);
				// Does this cookie string begin with the name we want?
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');



	var csrf_token = $("#django-data").data().CSRF;
	function writeRunes(){
		words = $("#runeText").val();
		$.ajax({
			url:"/home/",
			type:"POST",
			data:{"runeInput":words, csrfmiddlewaretoken:csrftoken},
			success: function(data){
				runeJson = jQuery.parseJSON(data)
				console.log(runeJson)
			},
			error: function(request, textStatus, errorThrown){
				console.log('textStatus ' + textStatus);
				console.log('errorThrown ' + errorThrown);
			}
		})
	}
	$("#runeButton").click(writeRunes);
});
