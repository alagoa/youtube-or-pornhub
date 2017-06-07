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

	window.onload = function () {

	


	


	var limit = 100000;    

	var y = 0;
	var data = []; var dataSeries = { type: "line" };
	var dataPoints = [];
	var xvalues = []; 
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

	for (var i = 1 ; i<=300 ; i++){
		xvalues.push(i);
	}

	$.ajax({
			url: 'http://10.0.2.15:5000/results',
			success: function (rdata) {
				
									
				var jdata = JSON.parse(rdata)

				
				
				dataPoints.push({
					x: xvalues,
					y: jdata.scalogram 
				});

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
				chart.render();
			}
		});
    }


}

dashboard.getClassification = function () {

}

dashboard.getDemoChart = function() {
	window.onload = function () {
    
    $.ajax({
			url: 'http://10.0.2.15:5000/results',
			success: function (rdata) {
				var jdata = rdata.scalogram ; 
				updateChart(jdata); 
			}
	});
   	
   	var updateChart = function(udata){
   		var limit = 100000;    //increase number of dataPoints by increasing this
	   
		   var y = 0;
		   var data = []; var dataSeries = { type: "line" };
		   var dataPoints = [];
		   for (var i = 0; i < limit; i += 1) {
		    y += (Math.random() * 10 - 5);
		    dataPoints.push({
		      x: i - limit / 2,
		      y: y                
		    });
		  }
		  dataSeries.dataPoints = dataPoints;
		  data.push(udata);   

		  var chart = new CanvasJS.Chart("achartContainer",
	    {
	      zoomEnabled: true,
	      title:{
	        text: "Stress Test: 100,000 Data Points" 
	      },
	      animationEnabled: true,
	      axisX:{
	        labelAngle: 30
	      },
	      
	      axisY :{
	        includeZero:false
	      },
	      
	      data: data  // random generator below
	      
	    });

    	chart.render();            
   	}

    
  }



  
   
  
}

