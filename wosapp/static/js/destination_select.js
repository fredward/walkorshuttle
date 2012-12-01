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
					//make the correct post here
				});
		$('#destination-select').change(function(){
					console.log($('#destination-select :selected').attr('id'));
					//make the correct post here
			});
	});
});