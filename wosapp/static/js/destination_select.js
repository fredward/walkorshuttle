//set up our thisination stop selection
$(document).ready(function() {
	//stop caching
	$.ajaxSetup({ cache: false });
	//get a list of all the stops
	$.ajax({
		url : "destinations/",
		dataType : "json",
	}).done(function(data) {
		
		//show the names of possible destinations
		var i = 0;
		$.each(data, function(){
			//add buttons and options to select -- buttons are the most popular stops
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
					//make the post call to python -- the random url prevents caching, mobile devices were being very stubborn
					$.ajax({
						url : "destination_selected/"+Math.random()*Math.random(),
						type : "POST",
						dataType : "json",
						data : {destination_id : $(this).attr('id')},
					
					}).done(function(data) {
						display_route_data(data);
					});
					toggleLoading('on');
				});
		$('#destination-select select').change(function(){
					//make the post call to python
				if($('#destination-select :selected').attr('id') != "default")
				{
					$.ajax({
						url : "destination_selected/",
						type : "POST",
						dataType : "json",
						data : {destination_id : $('#destination-select :selected').attr('id')},
					
					}).done(function(data) {
						display_route_data(data);
					});
					toggleLoading('on');
				}
			});
	});
});
//show the returned data on optimal routing -- and show error message if there is a failer
function display_route_data(data){
	if(data['success'] == 'success'){
	// take the data returned and display our route optimization
	// if we had a successful query
		$("#fastest-route-display").html("<strong>Fastest route with shuttles:</strong>"+
										"</br>1. Walk to "+data['fastest']['on_stop'] +
										"</br>2. Get on " + data['fastest']['route']+" in " + Math.round(data['fastest']['board_time']/60 *10)/10 + " min." + 
										"</br>3. Ride to "+data['fastest']['off_stop']+
										"</br>4. Walk to " +data['fastest']['end_stop']+
										"</br>Total time: "+Math.round(data['fastest']['total_time']/60 *10)/10 + " min."+
										"</br>Transit time: "+Math.round(data['fastest']['transit_time']/60 *10)/10 + " min.");
		$("#least-walking-display").html("<strong>Least walking with shuttles:</strong>"+
										"</br>1. Walk to "+data['least_walking']['on_stop'] +
										"</br>2. Get on " + data['least_walking']['route']+" in " + Math.round(data['least_walking']['board_time']/60 *10)/10 + " min." +  
										"</br>3. Ride to "+data['least_walking']['off_stop']+
										"</br>4. Walk to " + data['least_walking']['end_stop']+
										"</br>Total time: "+Math.round(data['least_walking']['total_time']/60 *10)/10 + " min." +
										"</br>Transit time: "+Math.round(data['least_walking']['transit_time']/60 *10)/10 + " min.");
		$("#least-transit-display").html("<strong>Least transit time:</strong>"+
										"</br>1. Walk to "+data['least_transit']['on_stop'] +
										"</br>2. Get on " + data['least_transit']['route']+" in " + Math.round(data['least_transit']['board_time']/60 *10)/10 + " min." +  
										"</br>3. Ride to "+data['least_transit']['off_stop']+
										"</br>4. Walk to " + data['least_transit']['end_stop']+
										"</br>Total time: "+Math.round(data['least_transit']['total_time']/60 *10)/10 + " min." +
										"</br>Transit time: "+Math.round(data['least_transit']['transit_time']/60 *10)/10 + " min.");
		$("#time-to-walk-display").html("<strong>Walking</strong>: "+Math.round(data['just_walking_time']/60 *10)/10 + " min.");
	}
	//handle some errors..
	else if(data['success'] == 'failed to load arrivals')
	{
		$("#time-to-walk-display").html("<strong>Walking</strong>: "+Math.round(data['just_walking_time']/60 *10)/10 + " min.");
		$("#fastest-route-display").html("<strong>Could not load arrival data for shuttles!</strong>");
		$("#least-walking-display").html('');
		$("#least-transit-display").html('');
	}
	else if(data['success'] == 'chose identity stop')
	{
		$("#time-to-walk-display").html("<strong>Walking</strong>: "+Math.round(data['just_walking_time']/60 *10)/10 + " min.");
		$("#fastest-route-display").html("<strong>You chose your closest stop!</strong>");
		$("#least-walking-display").html('');
		$("#least-transit-display").html('');

	}
	toggleLoading('off');
}
//toggle loading states
function toggleLoading(state){
	//disable inputs and show some loading text
	if(state == 'on')
	{
		$("#popular-destinations > .btn").attr("disabled", '');
		$("#destination-select > select").attr("disabled",'');
		//$("#route-display").text("Loading....");
		$("#route-display").show();
	}
	else if(state == 'off')
	{
		$("#popular-destinations > .btn").removeAttr("disabled");
		$("#destination-select > select").removeAttr("disabled");
	}
}