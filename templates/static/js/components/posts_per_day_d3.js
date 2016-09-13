"use strict"

var margin_posts = {top: 30, right: 40, bottom: 30, left: 50},
    width_posts = 900 - margin_posts.left - margin_posts.right,
    height_posts = 300 - margin_posts.top - margin_posts.bottom;

var parseDate_post = d3.time.format("%d-%b-%y").parse;

var xp = d3.time.scale().range([0, width_posts]);
var yp0 = d3.scale.linear().range([height_posts, 0]);

var xpAxis = d3.svg.axis().scale(xp)
    .orient("bottom").ticks(5);

var ypAxisLeft = d3.svg.axis().scale(yp0)
    .orient("left").ticks(5);

var valueline_post = d3.svg.line()
    .x(function(d) { return xp(d.date); })
    .y(function(d) { return yp0(d.close); });

var svg_posts = d3.select(".chart_posts")
        .attr("width", width_posts + margin_posts.left + margin_posts.right)
        .attr("height", height_posts + margin_posts.top + margin_posts.bottom)
    .append("g")
        .attr("transform",
              "translate(" + margin_posts.left + "," + margin_posts.top + ")");

// Get the data
d3.json("d3_posts_per_day/", function(error, data_posts) {
    console.log(data_posts);
    data_posts.forEach(function(d) {
        d.date = parseDate_post(d.date);
        d.close = d.close;
        d.open = +d.open;
    });

    // Scale the range of the data
    xp.domain(d3.extent(data_posts, function(d) { return d.date; }));
    yp0.domain([0, d3.max(data_posts, function(d) {
		return Math.max(d.close); })]);

    svg_posts.append("path")        // Add the valueline_post path.
        .attr("d", valueline_post(data_posts));

    svg_posts.append("g")            // Add the X Axis
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height_posts + ")")
        .call(xpAxis)

    svg_posts.append("g")
        .attr("class", "y axis")
        .style("fill", "black")
        .call(ypAxisLeft)
        .append("text")
        .text("people");

});