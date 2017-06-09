var dashboard = dashboard || {};



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
				url: 'http://10.0.2.15:5000/last-second-bytes',
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

	
	/*for (var i = -limit/2; i <= limit/2; i++) {
		y += (Math.random() * 10 - 5);
		dateTime = new Date(1960, 08, 15);

		// dateTime.setMilliseconds(dateTime.getMilliseconds() + i);
		// dateTime.setSeconds(dateTime.getSeconds() + i);
		// dateTime.setMinutes(dateTime.getMinutes() + i);
		// dateTime.setHours(dateTime.getHours() + i);
		dateTime.setDate(dateTime.getDate() + i);
		// dateTime.setMonth(dateTime.getMonth() + i);
		// dateTime.setFullYear(dateTime.getFullYear() + i);

		dataPoints.push({
			x: dateTime,
			y: y
		});
	}*/

	

	var updateChart = function() {
		$.ajax({
			url: 'http://10.0.2.15:5000/results',
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

