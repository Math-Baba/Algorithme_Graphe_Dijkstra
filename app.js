const API = "http://localhost:8080";
const svg = document.getElementById("graph");
const srcSel = document.getElementById("src");
const dstSel = document.getElementById("dst");

// nouveaux éléments
const nodeIdIn = document.getElementById("nodeId");
const nodeXIn = document.getElementById("nodeX");
const nodeYIn = document.getElementById("nodeY");
const nodeCapIn = document.getElementById("nodeCap");
const btnAddNode = document.getElementById("btnAddNode");

const edgeUIn = document.getElementById("edgeU");
const edgeVIn = document.getElementById("edgeV");
const edgeWIn = document.getElementById("edgeW");
const btnAddEdge = document.getElementById("btnAddEdge");


async function fetchGraph() {
  const g = await fetch(API + "/graph").then(r => r.json());
  drawGraph(g);
  updateSelects(g.nodes);
}

function drawGraph(g) {
  svg.innerHTML = "";
  g.edges.forEach(e => {
    const a = g.nodes[e.u], b = g.nodes[e.v];
    const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", a.x); line.setAttribute("y1", a.y);
    line.setAttribute("x2", b.x); line.setAttribute("y2", b.y);
    svg.appendChild(line);
  });
  Object.values(g.nodes).forEach(n => {
    const c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    c.setAttribute("cx", n.x); c.setAttribute("cy", n.y);
    c.setAttribute("r", 10); c.setAttribute("data-id", n.id);
    svg.appendChild(c);
  });
}

function updateSelects(nodes) {
  [srcSel, dstSel].forEach(sel => { sel.innerHTML = ""; });
  Object.keys(nodes).forEach(id => {
    [srcSel, dstSel].forEach(sel => {
      const o = document.createElement("option");
      o.value = id; o.textContent = id;
      sel.appendChild(o);
    });
  });
}

document.getElementById("btnColor").onclick = async () => {
  const res = await fetch(API + "/algo/coloring").then(r => r.json());
  document.querySelectorAll("circle").forEach(c => {
    const color = res[c.dataset.id];
    c.setAttribute("fill", ["#ccc", "#4CAF50", "#2196F3", "#FFC107"][color]);
  });
};

document.getElementById("btnPath").onclick = async () => {
  const src = srcSel.value, dst = dstSel.value;
  const res = await fetch(`${API}/algo/dijkstra?src=${src}&dst=${dst}`).then(r => r.json());
  const path = res.path;
  document.querySelectorAll("circle").forEach(c => {
    c.setAttribute("fill", path.includes(c.dataset.id) ? "red" : "steelblue");
  });
};

// remplir x,y en cliquant sur le SVG
svg.addEventListener("click", (e) => {
  const r = svg.getBoundingClientRect();
  const x = Math.round(e.clientX - r.left);
  const y = Math.round(e.clientY - r.top);
  nodeXIn.value = x;
  nodeYIn.value = y;
});

// fonctions d'envoi
async function addNode() {
  const id = nodeIdIn.value.trim();
  if (!id) { alert("id requis"); return; }
  const body = {
    id: id,
    x: Number(nodeXIn.value) || 0,
    y: Number(nodeYIn.value) || 0,
    capacity: Number(nodeCapIn.value) || 1
  };
  try {
    await fetch(API + "/graph/node", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    await fetchGraph();
  } catch (err) {
    console.error(err); alert("Erreur ajout nœud");
  }
}

async function addEdge() {
  const u = edgeUIn.value.trim();
  const v = edgeVIn.value.trim();
  if (!u || !v) { alert("u et v requis"); return; }
  const body = { u: u, v: v };
  const w = edgeWIn.value.trim();
  if (w !== "") body.weight = Number(w);
  try {
    await fetch(API + "/graph/edge", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });
    await fetchGraph();
  } catch (err) {
    console.error(err); alert("Erreur ajout arête");
  }
}

btnAddNode.addEventListener("click", (ev) => { ev.preventDefault(); addNode(); });
btnAddEdge.addEventListener("click", (ev) => { ev.preventDefault(); addEdge(); });

fetchGraph();
