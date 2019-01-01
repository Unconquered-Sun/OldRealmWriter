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
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
    data: {csrfmiddlewaretoken: csrftoken },
	});


	var csrf_token = $("#django-data").data().CSRF;
	function writeRunes(){
		console.log("TEST2")
		$.ajax({
			url:"/home/",
			type:"POST",
			data:{},
			success: function(data){
				console.log(data)
			},
			error: function(request, textStatus, errorThrown){
				console.log('textStatus ' + textStatus);
				console.log('errorThrown ' + errorThrown);
			}
		})
	}
	console.log("TEST1");
	$("#runeButton").click(writeRunes);
});
