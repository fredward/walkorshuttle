//set up our thisination stop selection
$(document).ready(function() {
	$.ajax({
		url : "destinations/",
		dataType : "json",
	}).done(function(data) {
		
		//show the names of possible destinations
		$.each(data, function(){
			if(this['name'] == 'Boylston Gate' || this['name'] == 'Quad' || this['name'] == 'Mather House' || this['name'] == 'Memorial Hall')
			{
				$('#popular-destinations').append($("<button/>", {text : this['name'], id : this['id'], class: "btn"}));
				
			}
			else{
				$('#destination-select').find('select').append($("<option/>", {text : this['name'], id: this['id']}));
				
			}
			
			
		});
		$('#popular-destinations > .btn').click(function(){
					console.log($(this).attr('id'));
					$.ajax({
						url : "destinationselected/"
						type : "POST",
						dataType : "json",
						data : {destination_id : $(this).attr('id')},
					
					}).done(function(data) {
					
					});
				});
		$('#destination-select').change(function(){
					console.log($('#destination-select :selected').attr('id'));
					//make the correct post here
					$.ajax({
						url : "destinationselected/"
						type : "POST",
						dataType : "json",
						data : {destination_id : $('#destination-select :selected').attr('id')},
					
					}).done(function(data) {
					
					});
			});
	});
});