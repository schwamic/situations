"use strict"

// variables
var margin_occupation = {top: 20, right: 30, bottom: 30, left: 40},
    width_occupation = 900 - margin_occupation.left - margin_occupation.right,
    height_occupation = 400 - margin_occupation.top - margin_occupation.bottom;

var xo = d3.scale.ordinal()
    .rangeRoundBands([0, width_occupation], .1);

var yo = d3.scale.linear()
    .range([height_occupation-160, 0]);

var xoAxis = d3.svg.axis()
    .scale(xo)
    .orient("bottom");

var yoAxis = d3.svg.axis()
    .scale(yo)
    .orient("left");

var chart_occupation = d3.select(".chart_occupation")
    .attr("width", width_occupation + margin_occupation.left + margin_occupation.right)
    .attr("height", height_occupation + margin_occupation.top + margin_occupation.bottom)
    .append("g")
    .attr("transform", "translate(" + margin_occupation.left + "," + margin_occupation.top + ")");

d3.json("d3_occupation/", function(error, data_occupation) {
    console.log(data_occupation);

  xo.domain(data_occupation.map(function(d) { return d.name; }));
  yo.domain([0, d3.max(data_occupation, function(d) { return d.value; })]);

  chart_occupation.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(10," + (height_occupation-160) + ")")
    .call(xoAxis)
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
      .call(yoAxis)
      .selectAll("text");
*/
  chart_occupation.selectAll(".bar")
      .data(data_occupation)
    .enter().append("rect")
      .attr("transform", "translate(10, 0)")
      .attr("x", function(d) { return xo(d.name); })
      .attr("y", function(d) { return yo(d.value); })
      .attr("height", function(d) { return height_occupation - yo(d.value) -160; })
      .attr("width", xo.rangeBand());
});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
  }