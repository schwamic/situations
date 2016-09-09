"use strict"

// variables
var data;
var JSONData;

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
    JSONData = [];
    for (var i = 0; i < data.length; i++){
       JSONData.push(data[i].fields);
    }

    // here you can use your data
    console.log(JSONData);

    //ZUWEISUNG DER DOMAINS
    x.domain(JSONData.map(function(d) { return d.occupation; }));
    y.domain([0, d3.max(JSONData, function(d) { return parseInt(d.longitude); })]);

    //ZEICHNEN DER ACHSEN
    // Zeichnen der x-Achse
    svg.append("g")
       .attr("class", "axis abscissa")
       .attr("transform",
     "translate(0, "+ (height - bottomPadding)+")")
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
    .data(data)
    .enter();

    // Säulendiagramm zeichnen
    barChart.append("rect")
       .attr("class", "bar")
       .attr("x", function(d) { return x(d.occupation); })
       .attr("y", height - bottomPadding )
       .attr("width", x.rangeBand())
       .attr("height", 0)


/**************** HIER FEHLER !! *************/
   // Animation der Balkenhöhe
   .transition()
   .delay(function(d, i) { return i * 80; })
   .duration(800)
   .attr("y", function(d) { return y(parseInt(d.longitude)); })
   .attr("height", function(d) {
    return height - bottomPadding - y(parseInt(d.longitude)); }
   );

    // Werte als SVG-Text in Säulen anzeigen und positionieren
    barChart.append("text")
       .attr("x", function(d) { return x(d.occupation); })
       .attr("y", function(d) { return y(parseInt(d.longitude)); })
       .attr("dx", x.rangeBand()/2)
       .attr("dy", "1.5em")
       .attr("text-anchor", "middle")
       .text(function(d) { return (d.longitude); });


});
