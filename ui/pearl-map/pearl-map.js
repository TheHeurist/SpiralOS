// SpiralOS Pearl Map viewer with responsive viewport sizing
const svgNode = document.getElementById("graph");

function measureViewport() {
  const bounds = svgNode.getBoundingClientRect();
  const width = Math.max(bounds.width || window.innerWidth, 320);
  const height = Math.max(bounds.height || Math.floor(window.innerHeight * 0.6), 320);
  return { width, height };
}

function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(null, args), delay);
  };
}

fetch("../../docs/ekr/lattice.json")
  .then(response => response.json())
  .then(lattice => {
    let { width, height } = measureViewport();
    const svg = d3.select(svgNode)
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("preserveAspectRatio", "xMidYMid meet");

    const nodes = lattice.map(p => ({ id: p.id, title: p.title }));
    const links = [];

    lattice.forEach(p => {
      (p.relations.children || []).forEach(c => {
        links.push({ source: p.id, target: c });
      });
      (p.relations.lateral || []).forEach(l => {
        links.push({ source: p.id, target: l });
      });
    });

    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(180))
      .force("charge", d3.forceManyBody().strength(-280))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.append("g")
      .attr("stroke", "rgba(100, 168, 255, 0.35)")
      .attr("stroke-width", 1.5)
      .selectAll("line")
      .data(links)
      .join("line");

    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("r", 12)
      .attr("fill", "#3cf")
      .attr("stroke", "#08142d")
      .attr("stroke-width", 2)
      .call(drag(simulation));

    const label = svg.append("g")
      .selectAll("text")
      .data(nodes)
      .join("text")
      .attr("class", "label")
      .attr("dy", -18)
      .attr("text-anchor", "middle")
      .text(d => d.title);

    node.append("title").text(d => d.id);

    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);

      label
        .attr("x", d => d.x)
        .attr("y", d => d.y);
    });

    function resize() {
      ({ width, height } = measureViewport());
      svg.attr("viewBox", `0 0 ${width} ${height}`);
      simulation.force("center", d3.forceCenter(width / 2, height / 2));
      simulation.alpha(0.5).restart();
    }

    window.addEventListener("resize", debounce(resize, 150));
  })
  .catch(error => {
    console.error("Failed to load lattice.json", error);
    const fallback = document.createElement("p");
    fallback.textContent = "Unable to load the knowledge lattice. Please refresh the page or check the network connection.";
    fallback.style.color = "#ff9f9f";
    fallback.style.textAlign = "center";
    fallback.style.padding = "1.5rem";
    svgNode.replaceWith(fallback);
  });

function drag(simulation) {
  function start(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }

  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }

  function end(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }

  return d3.drag()
    .on("start", start)
    .on("drag", dragged)
    .on("end", end);
}
