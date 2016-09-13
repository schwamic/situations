"use strict"

// variables
var amargin = {top: 20, right: 30, bottom: 30, left: 40};
var awidth = 900 - amargin.left - amargin.right;
var aheight = 400 - amargin.top - amargin.bottom;

var ya = d3.scale.ordinal()
    .rangeRoundBands([0,aheight], .1);

var xa = d3.scale.linear()
    .range([0,awidth]);

var xaAxis = d3.svg.axis()
    .scale(xa)
    .orient("bottom");

var yaAxis = d3.svg.axis()
    .scale(ya)
    .orient("left");

var chart_age = d3.select(".chart_age")
    .attr("width", awidth + amargin.left + amargin.right)
    .attr("height",aheight + amargin.top + amargin.bottom)
    .append("g")
    .attr("transform", "translate(" + amargin.left + "," + amargin.top + ")");


// get-request to endpoint d3_gender - hier muss nichts weiter gemacht werden. json-file passt!
d3.json("d3_age/", function(error, data) {
    console.log(data);

    xa.domain([0, d3.max(data, function(d) { return d.publications; })]);
    ya.domain(data.map(function(d) { return d.age; }));
/*
    chart_age.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(10," + aheight +")")
        .call(xaAxis)
*/
    chart_age.append("g")
      .attr("class", "y axis")
      .call(yaAxis)
      .selectAll("text");

    chart_age.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("transform", "translate(0, 15)")
      .attr("y", function(d) { return ya(d.age); })
      .attr("height", 30)
      .attr("width", function(d) { return xa(d.publications); })

});

function type(d) {
  d.publications = +d.publications; // coerce to number
  return d;
}





/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// EXAMPLE 1
var width = 420,
    barHeight = 20;

var x = d3.scale.linear()
    .range([0, width]);

var chart = d3.select(".chart")
    .attr("width", width);

// get-request to endpoint d3_data
d3.json("d3_data/", function(error, d3_data) {

    // parse string to json
    data = JSON.parse(d3_data);

    // load just the fields in an array -> clean json
    data_age = [];
    for (var i = 0; i < data.length; i++){
       data_age.push(data[i].fields);
    }

    // here you can use your data
    console.log(data_age);
    x.domain([0, d3.max(data_age, function(d) { return d.latitude; })]);

  chart.attr("height", barHeight * data_age.length);

  var bar = chart.selectAll("g")
      .data(data_age)
    .enter().append("g")
      .attr("transform", function(d, i) { return "translate(0," + i * barHeight + ")"; });

  bar.append("rect")
      .attr("width", function(d) { return x(d.latitude); })
      .attr("height", barHeight - 1);

  bar.append("text")
      .attr("x", function(d) { return x(d.latitude) - 3; })
      .attr("y", barHeight / 2)
      .attr("dy", ".35em")
      .text(function(d) { return d.latitude; });

});

function type(d) {
  d.value = +d.value; // coerce to number
  return d;
}

*/


/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// T3N - EXAMPLE 2 - GEHT NICHT ! ! ! ! ! !
// variables
var data;
var data_age;

//DIMENSIONEN DES DIAGRAMMS
var width = 600, height = 300;
var padding = 20, leftPadding = 100, bottomPadding = 120;

//SKALIERUNG DER ACHSEN
var x = d3.scale.ordinal()
    .rangeRoundBands([leftPadding, width - padding],0.1);
var y = d3.scale.linear()
    .range([height - bottomPadding, padding]);

//DEFINITION DER ACHSEN
var abscissa = d3.svg.axis().scale(x).orient("bottom");
var ordinate = d3.svg.axis().scale(y).orient("left");

//DEFINITION DES SVG ELEMENTS
var svg = d3.select("#bar-chart").append("svg")
     .attr("width", width).attr("height", height);


// get-request to endpoint d3_data
d3.json("d3_data/", function(error, d3_data) {

    // parse string to json
    data = JSON.parse(d3_data);

    // load just the fields in an array -> clean json
    data_age = [];
    for (var i = 0; i < data.length; i++){
       data_age.push(data[i].fields);
    }

    // here you can use your data

    console.log(data_age);
    //ZUWEISUNG DER DOMAINS

    var latitudeFn = function(d) { return d.latitude }
    var nameFN = function(d) { return d.name }
    var xNameFN = function(d) { return x(d.name); }
    var ylatitudeFN = function(d) { console.log((d.latitude)); return y(d.latitude); }

    x.domain(data_age.map(nameFN));
    y.domain([0, d3.max(data_age, latitudeFn)]);

    //ZEICHNEN DER ACHSEN
    // Zeichnen der x-Achse
    svg.append("g")
       .attr("class", "axis abscissa")
       .attr("transform", "translate(0, "+ (height - bottomPadding)+")")
       .call(abscissa)

     // Positionierung der Label
       .selectAll("text")
       .style("text-anchor", "end")
       .attr("dx", "-.5em")
       .attr("dy", ".15em")
       .attr("transform", function(d)
        { return "rotate(-25)" }
        );

    // Zeichnen der y-Achse
    svg.append("g")
       .attr("class", "axis ordinate")
       .attr("transform", "translate("+(leftPadding)+", 0)")
       .call(ordinate);

    //ZEICHNEN DES DIAGRAMMS
    var barChart = svg.selectAll("rect")
        .data(data_age)
        .enter();

    // Säulendiagramm zeichnen
    barChart.append("rect")
       .attr("class", "bar")
       .attr("x", x(nameFN))
       .attr("y", height - bottomPadding )
       .attr("width", x.rangeBand())
       .attr("height", 0)

    // Animation der Balkenhöhe
       .transition()
       .delay(function(d, i) { return i * 80; })
       .duration(800)
       .attr("y", latitudeFn)
       .attr("height", function(d) {
        return height - bottomPadding - y(d.latitude); }
       );

    // Werte als SVG-Text in Säulen anzeigen und positionieren
    barChart.append("text")
       .attr("x", xNameFN)
       .attr("y", ylatitudeFN)
       .attr("dx", x.rangeBand()/2)
       .attr("dy", "1.5em")
       .attr("text-anchor", "middle")
       .text(function(d) { return (d); });

});
*/