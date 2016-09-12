"use strict"

// variables
var width = 960,
    height = 500,
    radius = Math.min(width, height) / 2;

var color = d3.scale.ordinal()
    .range(["#fff"]);

var arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

var labelArc = d3.svg.arc()
    .outerRadius(radius - 40)
    .innerRadius(radius - 40);

var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.publications; });

var svg = d3.select(".chart_gender")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");


// get-request to endpoint d3_gender - hier muss nichts weiter gemacht werden. json-file passt!
d3.json("d3_gender/", function(error, data_gender) {
    if (error) throw error;
    console.log(data_gender);

  var g = svg.selectAll(".arc")
      .data(pie(data_gender))
    .enter().append("g")
      .attr("class", "arc");

  g.append("path")
      .attr("d", arc)
      .style("fill", function(d) { return color(d.value); })
      .style("stroke", "black");

  /*g.append("text")
      .attr("transform", function(d) { return "translate(" + labelArc.centroid(d) + ")"; })
      .attr("dy", ".35em")
      .text(function(d) { return d.value; });*/
});

function type(d) {
  d.publications = +d.publications;
  return d;
}