var dashboard = dashboard || {};

var apiurl = 'http://172.18.0.1:5000'

dashboard.getGraph = function () {


    window.onload = function () {

		

		var dps = []; // dataPoints

		var chart = new CanvasJS.Chart("chartContainer", {
			title: {
				text: "Upload/Download live"
			},
			data: [{
				type: "line",
				dataPoints: dps
			}]
		});

		var xVal = 0;
		var yVal = 1000;	
		var updateInterval = 1000;
		var dataLength = 60*5; // number of dataPoints visible at any point

		var updateChart = function (count) {

			$.ajax({
				url: apiurl+'/last-second-bytes',
				success: function (data) {
					count = count || 1;
										
					var jdata = JSON.parse(data)

					dps.push({
							x: xVal,
							y: jdata.download
						});
					xVal++;
					if (dps.length > dataLength) {
						dps.shift();
					}

					chart.render();	
				}
			});
			
				

		};

		// generates first set of dataPoints
		updateChart(dataLength); 

		// update chart after specified time. 
		setInterval(function(){updateChart()}, updateInterval); 

	}


}

dashboard.getScalogram = function () {

	var windowload = window.onload;

	window.onload = function () {

	windowload.call(this);	

	
	
	
}

	var updateIntervalC = 1000 * 60; 	

	var updateChart = function() {
		$.ajax({
			url: apiurl+'/results',
			success: function (rdata) {

				var limit = 100000;    

				var y = 0;
				var data = []; var dataSeries = { type: "line" };
				var dataPoints = [];
				var xvalues = []; 
				var jdata = JSON.parse(rdata);

				for (var i = 1 ; i<=300 ; i++){
					//xvalues.push(i);
					dataPoints.push({
					x: i,
					y: jdata.scalogram[i-1] 
				});
				}
				
									
				
				
				dashboard.getClassification(jdata.service)		
				

				dataSeries.dataPoints = dataPoints;
				
				data.push(dataSeries);   
				

				var chart = new CanvasJS.Chart("scalogramContainer",
				{
					zoomEnabled: true,
					animationEnabled: true,
					title:{
						text: "last generated scalogram" 
					},
					axisX :{
						labelAngle: -30
					},
					axisY :{
						includeZero:false
					},
					data: data  

					
				});  

				console.log(data);
				chart.render();
		          
				
			}
		});

	}

	updateChart(); 
	// update chart after specified time. 
	setInterval(function(){updateChart()}, updateIntervalC); 
	
    


}

dashboard.getClassification = function ( service ) {
	
	var img = $("#serviceimg")[0];
	console.log(img); 

	if(service == "YouTube"){
		img.src = "assets/img/youtube.png";
	}
	else if(service == "Spotify"){
		img.src = "assets/img/spotify.png";
	}
	else if(service == "PornHub"){
		img.src = "assets/img/pornhub.jpg";
	}
	else{
		img.src = "assets/img/chrome.png";
	}


	

}

