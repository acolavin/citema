#!/usr/bin/python
import os, sys
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import subprocess
import citema

print 'Content-type: text/html\n'
print 'Loading ... don\'t go anywhere!'
sys.stdout.flush()
os.chdir('/afs/ir.stanford.edu/users/a/c/acolavin/cgi-bin/')
arguments = cgi.FieldStorage()
pmid = 23874166
level = 2
if 'pmid' in arguments:
    pmid = int(arguments['pmid'].value)
if 'level' in arguments:
    level = int(arguments['level'].value)
citema.makeMap(pmid,level)

print '''
<meta charset="utf-8">
<style>

.noder {
  stroke: #fff;
  stroke-width: 1.5px;
}

.link {
  stroke: #999;
  stroke-opacity: .6;
}

</style>
<body>
<script src="http://d3js.org/d3.v3.min.js"></script>
<script>

var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(20)
    .size([width, height]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("../%i.json", function(error, graph) {
  force
      .nodes(graph.nodes)
      .links(graph.links)
      .start();

  var link = svg.selectAll(".link")
      .data(graph.links)
    .enter().append("line")
      .attr("class", "link")
      .style("stroke-width", 2);//function(d) { return Math.sqrt(d.value); });

  var node = svg.selectAll("a.node")
      .data(graph.nodes)
    .enter().append("circle")
      .attr("class", "noder")
      .attr("r", function(d) { return Math.sqrt(d.value); })
      .style("fill", function(d) { return color(d.group); })
      .call(force.drag);
      //      .on("click", function(d) { window.location = d.url });

  node.append("title")
      .text(function(d) { return d.name; });

/*
  node.append("svg:a")
    .attr("xlink:href", function(d){return d.url;})
    .append("svg:rect")
    .attr("y", -barHeight / 2)
    .attr("height", barHeight)
    .attr("width", barWidth);
*/

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
});

</script>''' % pmid

