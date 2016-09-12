"use strict"

// variables
var margin = {top: 20, right: 30, bottom: 30, left: 40},
    width = 960 - margin.left - margin.right,
    height = 700 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height-160, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var chart_occupation = d3.select(".chart_occupation")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json("d3_occupation/", function(error, data) {
    console.log(data);

  x.domain(data.map(function(d) { return d.name; }));
  y.domain([0, d3.max(data, function(d) { return d.value; })]);

  chart_occupation.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(10," + (height-160) + ")")
    .call(xAxis)
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.5em")
    .attr("dy", ".15em")
    .attr("transform", function(d)
    { return "rotate(-50)" }
    );

/*
  chart_occupation.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .selectAll("text");
*/
  chart_occupation.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("transform", "translate(10, 0)")
      .attr("x", function(d) { return x(d.name); })
      .attr("y", function(d) { return y(d.value); })
      .attr("height", function(d) { return height - y(d.value) -160; })
      .attr("width", x.rangeBand());
});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
  }