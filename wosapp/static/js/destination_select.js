//set up our thisination stop selection
$(document).ready(function() {
	$.ajax({
		url : "destinations/",
		dataType : "json",
	}).done(function(data) {
		
		//show the names of possible destinations
		var i = 0;
		$.each(data, function(){
			//add buttons and options to select
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
					//make the post call to python
					$.ajax({
						url : "destination_selected/",
						type : "POST",
						dataType : "json",
						data : {destination_id : $(this).attr('id')},
					
					}).done(function(data) {
						display_route_data(data);
					});
					toggleLoading('on');
				});
		$('#destination-select').change(function(){
					//make the post call to python
					$.ajax({
						url : "destination_selected/",
						type : "POST",
						dataType : "json",
						data : {destination_id : $('#destination-select :selected').attr('id')},
					
					}).done(function(data) {
						display_route_data(data);
					});
					toggleLoading('on');

			});
	});
});
//show the returned data on optimal routing
function display_route_data(data){
	//$('#route-display').text(data['route_string']);
}

function toggleLoading(state){
	//disable inputs and show some loading text
	if(state == 'on')
	{
		$("#popular-destinations > .btn").attr("disabled", '');
		$("#destination-select > select").attr("disabled",'');
		$("#route-display").text("Loading....");
		$("#route-display").show();
	}
	else if(state == 'off')
	{
		$("#popular-destinations > .btn").removeAttr("disabled");
		$("#destination-select > select").removeAttr("disabled");
	}
}