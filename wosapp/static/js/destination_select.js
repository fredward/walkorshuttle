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
	// take the data returned and display our route optimization
	//$("#route-display").text('');
	$("#fastest-route-display").html("<strong>Fastest route with shuttles:</strong>"+
									"</br>1. Walk to "+data['fastest']['on_stop'] +
									"</br>2. Get on " + data['fastest']['route']+  
									"</br>3. Ride to "+data['fastest']['off_stop']+
									"</br>4. Walk to " +data['fastest']['end_stop']+
									"</br>Total time: "+Math.round(data['fastest']['total_time']/60 *10)/10 + " min.");
	$("#least-walking-display").html("<strong>Least walking:</strong>"+
									"</br>1. Walk to "+data['least_walking']['on_stop'] +
									"</br>2. Get on " + data['least_walking']['route']+  
									"</br>3. Ride to "+data['least_walking']['off_stop']+
									"</br>4. Walk to " +data['least_walking']['end_stop'] +
									"</br>Total time: "+Math.round(data['least_walking']['total_time']/60 *10)/10 + " min.");
	$("#time-to-walk-display").html("<strong>Walking</strong>: "+Math.round(data['just_walking_time']/60 *10)/10 + " min.");
	toggleLoading('off');
}

function toggleLoading(state){
	//disable inputs and show some loading text
	if(state == 'on')
	{
		$("#popular-destinations > .btn").attr("disabled", '');
		$("#destination-select > select").attr("disabled",'');
		$("#fastest-route-display").text("Loading....");
		$("#route-display").show();
	}
	else if(state == 'off')
	{
		$("#popular-destinations > .btn").removeAttr("disabled");
		$("#destination-select > select").removeAttr("disabled");
	}
}