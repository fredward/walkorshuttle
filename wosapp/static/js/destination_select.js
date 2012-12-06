//set up our thisination stop selection
$(document).ready(function() {
	$.ajax({
		url : "destinations/",
		dataType : "json",
	}).done(function(data) {
		
		//show the names of possible destinations
		var i = 0;
		$.each(data, function(){
			if(this['name'] == 'Boylston Gate' || this['name'] == 'Quad' || this['name'] == 'Mather House' || this['name'] == 'Memorial Hall')
			{
				$('#popular-destinations').append($("<button/>", {text : this['name'], id : this['id'], class: "btn", style: "margin-bottom: 5px"}));
				i++;
				//break up our button group
				if(i==2)
				{
					$('#popular-destinations').append($("<br/>"));
				}
					
				
			}
			else{
				$('#destination-select').find('select').append($("<option/>", {text : this['name'], id: this['id']}));
				
			}
			
			
		});
		$('#popular-destinations > .btn').click(function(){
					$.ajax({
						url : "destination_selected/",
						type : "POST",
						dataType : "json",
						data : {destination_id : $(this).attr('id')},
					
					}).done(function(data) {
					
					});
				});
		$('#destination-select').change(function(){
					//make the correct post here
					$.ajax({
						url : "destination_selected/",
						type : "POST",
						dataType : "json",
						data : {destination_id : $('#destination-select :selected').attr('id')},
					
					}).done(function(data) {
					
					});
			});
	});
});