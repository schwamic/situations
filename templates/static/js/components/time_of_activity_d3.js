var margin_time = {top: 30, right: 40, bottom: 30, left: 50},
    width_time = 900 - margin_time.left - margin_time.right,
    height_time = 300 - margin_time.top - margin_time.bottom;

//var formatHours = d3.time.format("%X");

var xt = d3.time.scale().range([0, width_time]);
//var yt0 = d3.time.scale().range([height_time, 0]);
var yt0 = d3.scale.linear().range([height_time, 0]);

var xtAxis = d3.svg.axis()
    .scale(xt)
    .orient("bottom")
    .ticks(5);

/*var ytAxisLeft = d3.svg.axis()
    //.scale(yt0)
    .orient("left")
    .ticks(5);
    */
var ytAxisLeft = d3.svg.axis().scale(yt0)
    .orient("left").ticks(4);


var valueline_time = d3.svg.line()
    .x(function(d) { return xt(d.date); })
    .y(function(d) { return yt0(d.close); });

var svg_time = d3.select(".chart_time")
        .attr("width", width_time + margin_time.left + margin_time.right)
        .attr("height", height_time + margin_time.top + margin_time.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin_time.left + "," + margin_time.top + ")");

// Get the data
d3.json("d3_time_of_activity/", function(error, data_time) {
    console.log(data_time)

    var parseDate_time = d3.time.format("%Y-%m-%d");
    //var parseTime_time = d3.time.format("%X");

    data_time.forEach(function(d) {
        d.date = parseDate_time.parse(d.date);
        //d.close = parseTime_time.parse(d.close);
        d.close = d.close;
    });

    // Scale the range of the data
    xt.domain(d3.extent(data_time, function(d) { return d.date; }));
    //yt0.domain(d3.extent(data_time, function(d) { return (d.close); }));
    yt0.domain([0, d3.max(data_time, function(d) {
		return Math.max(d.close); })]);

    svg_time.append("path")        // Add the valueline_time path.
        .attr("d", valueline_time(data_time));

    svg_time.append("g")            // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height_time + ")")
        .call(xtAxis);

    svg_time.append("g")
        .attr("class", "y axis")
        .style("fill", "black")
        .call(ytAxisLeft)
        .append("text")
        .text("hours");
});