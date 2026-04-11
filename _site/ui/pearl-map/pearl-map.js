// Simple D3 viewer for SpiralOS lattice.json
fetch("../../docs/ekr/lattice.json")
  .then(r => r.json())
  .then(lattice => {
    const width = innerWidth, height = innerHeight;
    const svg = d3.select("#graph").attr("width", width).attr("height", height);

    const nodes = lattice.map(p => ({ id: p.id, title: p.title }));
    const links = [];
    lattice.forEach(p => {
      (p.relations.children || []).forEach(c =>
        links.push({ source: p.id, target: c }));
      (p.relations.lateral || []).forEach(l =>
        links.push({ source: p.id, target: l }));
    });

    const sim = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(180))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width/2, height/2));

    const link = svg.append("g").attr("stroke","#444")
      .selectAll("line").data(links).join("line");

    const node = svg.append("g")
      .selectAll("circle").data(nodes).join("circle")
      .attr("r",12).attr("fill","#3cf")
      .call(drag(sim));

    const label = svg.append("g")
      .selectAll("text").data(nodes).join("text")
      .attr("class","label").attr("dy",-18)
      .text(d=>d.title);

    node.append("title").text(d=>d.id);

    sim.on("tick",()=>{
      link.attr("x1",d=>d.source.x).attr("y1",d=>d.source.y)
          .attr("x2",d=>d.target.x).attr("y2",d=>d.target.y);
      node.attr("cx",d=>d.x).attr("cy",d=>d.y);
      label.attr("x",d=>d.x).attr("y",d=>d.y);
    });

    function drag(sim){
      function start(e){ if(!e.active) sim.alphaTarget(0.3).restart(); e.subject.fx=e.subject.x; e.subject.fy=e.subject.y;}
      function drag(e){ e.subject.fx=e.x; e.subject.fy=e.y;}
      function end(e){ if(!e.active) sim.alphaTarget(0); e.subject.fx=null; e.subject.fy=null;}
      return d3.drag().on("start",start).on("drag",drag).on("end",end);
    }
  });
