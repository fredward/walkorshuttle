//show more route info
$(document).ready( function() {

	$(".route-info").click( function() {
		$(this).find(".extra-route-prompt").hide();
		$(this).find(".extra-route-info").slideDown();
	}); 

});