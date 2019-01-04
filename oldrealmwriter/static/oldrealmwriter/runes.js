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

	function writeRunes(){
		words = $("#runeText").val();
		$.ajax({
			url:"/home/",
			type:"POST",
			data:{"runeInput":words, csrfmiddlewaretoken:csrftoken},
			success: function(data){
				runeJson = jQuery.parseJSON(data)
				console.log(runeJson)
				$("#runeDir").html("");
				
				// Create Table for Runes . Each table can hold 6 runes
				runeCount = runeJson["images"].length;
				//Determine number of tables 
				tableCount = Math.ceil(runeCount/6);
				for (var x=0; x<tableCount; x++){
					$("#runeDir").append('<table id="runeTable'+x+'"></table>');
					ids = [];
					for (var y = 0; y < 6; y++){
						newId = y+(x*6);
						ids.push(newId);
					};
					$("#runeTable"+x).append('<tr><td id="runeCell'+ids[0]+'"></td><td id="runeCell'+ids[1]+'"></td></tr>');
					$("#runeTable"+x).append('<tr><td id="runeCell'+ids[2]+'"></td><td id="runeCell'+ids[3]+'"></td></tr>');
					$("#runeTable"+x).append('<tr><td id="runeCell'+ids[4]+'"></td><td id="runeCell'+ids[5]+'"></td></tr>');
				}

				for (var index in runeJson["images"] ){
					// var image = new Image()
					// image.src() = 'data:image/png;base64,'+runeJson["images"][index]
					imageHtml = '<img src="data:image/png;base64,'+runeJson["images"][index]+'" id="rune'+index+'"/>'
					$("#runeCell"+index).append(imageHtml)
					$("#rune"+index).css("width","100px").css("height","150px")
				}
			},
			error: function(request, textStatus, errorThrown){
				console.log('textStatus ' + textStatus);
				console.log('errorThrown ' + errorThrown);
			}
		})
	}
	$("#runeButton").click(writeRunes);
});
