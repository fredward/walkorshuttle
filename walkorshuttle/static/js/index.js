//show more route info
$(document).ready( function() {

	$(".route-info").click( function() {
				 	console.log("test");
		$(this).find(".extra-route-prompt").hide();
		$(this).find(".extra-route-info").slideDown();

	}); 

});