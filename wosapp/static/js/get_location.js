// using jQuery
// Django provided code for managing sessions and cookies
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
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


function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
	    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	}
    });
//end of Django provided code for managing sessions and cookies 

//we asynchronously update data on the user's closest stop as the geolocation data comes in
//this lets other parts of the page load even if the geolocation data isn't fast
if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
					     function( position ) {
						 console.log(position);
						 //post to python script and use response to update displayed shuttle data
						 $.post("geolocate/",position,
							function(data) {
								//console.log(data['closest'])
							    $('#closest').text(data['closest']);
							    $.each(data['next_shuttles'], function(){
							    	//display the next shuttles to the users closest stop
							    	//under each stop show the next few stops for each shuttle after the users closest stop
							    	$('#next_shuttles').append($("<div/>", { text: (this[0] + ", " + this[1]), class : 'shuttle-info'}));
							    	next_stops = data['next_shuttles_route'][this[2]];
							    	console.log(next_stops)
							    	if(next_stops !== undefined) {
							    	$.each(next_stops, function() {
							    		
							    		$('#next_shuttles').append($("<div/>", { text: ("Next: "+this[0] + ", " + this[1]+", " +this[2]), class : 'shuttle-info'}));
							    	
							    	});}
							    });
							    $('.shuttle-info').click( function() {
							    	
							    });
							    //$('#next_shuttles').html(shuttle_string);
							}, 'json'
							);
					     },
					     function( error ) {
						 //Do something on error
					     },
					     {
						 timeout: (2 * 1000),
						 maximumAge: (1000 * 60 * 15),
						 enableHighAccuracy: true,
					     }
					     );
}
						     
					    
					  
