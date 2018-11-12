
function visualData(data){

	// console.log(data)	
	/*
	var pathToCSV = "price_range.csv"
	csvContent = download_csv(data,pathToCSV)
	console.log(csvContent)
	*/

	var coordinates = [];
	for (var i=0; i<data.length; i++){
		coordinates.push( [data[i][2] ,data[i][3]]);	
	}
	console.log("===> "+coordinates.length)
	updateMarkers(coordinates);

	//--------------------------------------
	// Layout Settings
	var margin = {top:50, right:50, bottom:0, left:50},
		width = 960 - margin.left - margin.right,
		height = 500 - margin.top - margin.bottom;

	var histHeight = height/5;


	var svg = d3.select("#viz")
				.append("svg")
				.attr("width", width + margin.left + margin.right)
				.attr("height", height + margin.top + margin.top)


	var plot = svg.append("g")
				  .attr("class", "plot")
				  // .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
				  .attr("transform", "translate(0, 0)");

	var x;
	var y;
	var colors;
	var handle;
	var dataset;
	var xx;
	
	//----------------
	// Read data from csv file
	//d3.csv(pathToCSV, prepare, function(data) {


	// color range
	colors = d3.scaleQuantize()
		   		 .domain([0, d3.max(data, function(d) {
		   		 	// console.log(d[1]);
		   		 	return d[1];
		   		 })])
		   		 .range(['#2B00E5','#2711D9','#2322CD','#1F34C1','#1B45B5','#1756A9','#13689D','#0F7991','#0B8A85','#079C79','#03AD6D','#00BF61'])


	var aa = 12

	x = d3.scaleLinear()
		  .domain([0, d3.max(data, function(d) {return d[1];})])
		  .range([0, width])
		  .clamp(true);

	xx = x

	// y scale for histogram
	y = d3.scaleLinear()
	  	  .range([histHeight, 0]);

	////  Histogram Set Up  ////

	////////TEST
	nn = 11
	minR= d3.min(data, function(d) {return d[1];});
	maxR= d3.max(data, function(d) {return d[1];});
	thresh = d3.range(minR, maxR, (maxR-minR)/nn	);
	start = [];
	prc   = [];
	for (var i = 0; i <= nn; i++ ){
		prc.push(minR + (maxR-minR)/nn*i);
	}
	////////////


	// set parameters
	var histogram = d3.histogram()
					  .value(function(d) {return d[1];})
					  // .domain(x.domain())
					   .thresholds(thresh);

	var hist = svg.append("g")
				  .attr("class", "histogram")
				  .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


	// group data for bars
	var bins = histogram(data);

	// y domain based on binned data
	y.domain([0, d3.max(bins, function(d) {return d.length;})]);

	var bar = hist.selectAll(".bar")
				  .data(bins)
				  .enter()
				  .append("g")
				  .attr("class", "bar")
				  // .attr("transform", "translate(50, 50)");
				  .attr("transform", function(d) {
				  	start.push(x(d.x0)); 
				  	return "translate(" + x(d.x0) + "," + y(d.length) + ")"; });

	bar.append("rect")
	   .attr("class", "bar")
	   .attr("x", 1)
	   .attr("y", 50)
	   .attr("width", function(d) {return x(d.x1) - x(d.x0) - 1;})
	   // console.log(x(d.x1) - x(d.x0) - 1);
	   // .attr("width", function(d) {return (x(d.x1) - x(d.x0))/1000;})
	   .attr("height", function(d) {return histHeight - y(d.length);})
	   .attr("fill", function(d) {return colors(d.x0);});

	bar.append("text")
	   .attr("dy", ".75em")
	   .attr("y", "50")
	   .attr("x", function(d) {return (x(d.x1) - x(d.x0))/2;})
	   .attr("text-anchor", "middle")
	   .text(function(d) {if (d.length > 5) return d.length;})
	   .style("fill", "white");


	/////////   Slider   //////////
	var currentValue = 0;

	var slider = svg.append("g")
					.attr("class", "slider")
					.attr("transform", "translate(" + margin.left + "," + (margin.top + histHeight + 55) + ")");

	dataset = data;
	drawPlot(dataset);

	const brush = d3.brushX()
				  .extent([[0, 0], [width, 40]])
				  .on("brush", brushed);

	slider.append("rect")
		  .attr("class", "drag-bar")
		  .attr("x", 0)
		  .attr("y", 0)
		  .attr("width", width)
		  .attr("height", 10)
		  .attr("fill", "#dcdcdc")
		  .attr("rx", 4)
		  .attr("ry", 4);

	slider.append("g", ".track-overlay")
		  .attr("class", "ticks")
		  .attr("transform", "translate(0, 18)")
		  .selectAll("text")
		  .data(x.ticks(nn))
		  // .data(bins)
		  .enter()
		  .append("text")
		  .attr("x", x)
		  .attr("y", 10)
		  .attr("text-anchor", "middle")
		  .text(function(d) {return d;});


	slider.append("g")
		  .attr("class", "brush")
		  .call(brush)
		  .call(brush.move, x.range());
	
	//})


	function drawPlot(data) {
		var locations = plot.selectAll(".location")
						    .data(data, function(d) { return d[0];});

		locations.exit().remove();
		// if filtered dataset has more circles than already existing, 
		// transition new ones in
		locations.enter()
				.append("circle")
				.attr("class", "location")
				// .attr("cx", function(d) {return x(d.price) + width/nn;})
				.attr("cx", function(d,i) {
					for (var k=0; k<= prc.length-1; k++){
						if (d[1]==prc[k] ||((d[1] > prc[k]) && (d[1] <= prc[k+1]))){
							break;
						}
					}
					return (start[k]+width/24+margin.left); })
				.attr("cy", function(d) {return Math.random() * ((height/2 + 50) - (height/2 - 50)) + (height/2 - 50) + 50;})
				.style("fill", function(d) {return colors(d[1]);})
				.style("stroke", function(d) {return colors(d[1]);})
				.style("opacity", 0.3)
				.attr("r", 5)
					.transition()
					.duration(400)
					.attr("r", 15)
						.transition()
						.attr("r", 5);

		// if filtered dataset has less circles than already existing,
		// remove excess
		locations.exit()
				 .remove();
	}

	function prepare(d) {
		console.log(d)
		d.price = +d.price;
		d.id = +d.id;
		d.lat = +d.latitude;
		d.long = +d.longitude;
		return d;
	}

	function brushed() {
		const position = d3.event.selection;
		const min = position[0];
		const max = position[1];
		update(min, max);
	}

	function update(min, max) {
		const valMin = x.invert(min);
		const valMax = x.invert(max);
		var coordinates = [];
		const newData = dataset.filter(function(d) {
			if (d[1] < valMax && d[1] > valMin){
				coordinates.push([d[2],d[3]]);	
			}
			return d[1] < valMax && d[1] > valMin;
		});

		updateMarkers(coordinates);
		drawPlot(newData);

		d3.selectAll(".bar")
		  .attr("fill", function(d) {return (d.x0 < valMax && d.x1 > valMin) ? colors(d.x0) : "#eaeaea"});
	}


	function download_csv(data,name) {
	    var csv = 'id,price,latitude,longitude\n';
	    data.forEach(function(row) {
	            csv += row.join(',');
	            csv += "\n";
	    });
	 
	    var hiddenElement = document.createElement('a');
	    hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);
	    hiddenElement.target = '_blank';
	    hiddenElement.download = name;
	    hiddenElement.click();

	    return csv;
	}

}







