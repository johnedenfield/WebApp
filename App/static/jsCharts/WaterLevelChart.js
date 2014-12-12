function WaterLevelChart(mydata) {


    	var data = new google.visualization.DataTable();
     	data.addColumn('datetime', 'Time(long)');
    	data.addColumn('number', 'Water Level');
	data.addColumn('number', 'Low Water Level');
	
	n=mydata.length;
	for (i =0; i < n; i++){
		row = mydata[i];
		var dtestr =row[0,0];
		var d = new Date(dtestr);
		data.addRow([d,row[0,1],2]);
	
	}  
    

    	 var options = {
		height: 500,		
		 hAxis: { title: 'Time'},
		 vAxis: { title: "Water Level", 
		  	  viewWindowMode:'explicit',
		  	  viewWindow:{max:3.5, min:0.0} }
     		};

	ChartId=document.getElementById('ex0');
	console.log(ChartId);
	var chart = new google.visualization.LineChart(ChartId);

     chart.draw(data, options);

   }
