const API_BASE_URL = 'http://localhost:5000';

// État de l'application
let graphData = null;
let coloringData = null;
let dijkstraPath = null;
let canvas, ctx;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    canvas = document.getElementById('graph-canvas');
    ctx = canvas.getContext('2d');
    
    // Ajuster la taille du canvas
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Événements
    document.getElementById('btn-load-graph').addEventListener('click', loadGraph);
    document.getElementById('btn-clear').addEventListener('click', clearVisualization);
    document.getElementById('btn-coloring').addEventListener('click', applyColoring);
    
    document.getElementById('form-add-node').addEventListener('submit', addNode);
    document.getElementById('form-add-edge').addEventListener('submit', addEdge);
    document.getElementById('form-add-constraint').addEventListener('submit', addConstraint);
    document.getElementById('form-dijkstra').addEventListener('submit', calculateDijkstra);
});

function resizeCanvas() {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth - 40;
    canvas.height = container.clientHeight - 40;
    if (graphData) {
        drawGraph();
    }
}

// Charger le graphe depuis l'API
async function loadGraph() {
    try {
        const response = await fetch(`${API_BASE_URL}/graph`);
        const data = await response.json();
        graphData = data;
        console.log('Données reçues:', data);
        const nodeCount = Object.keys(data.nodes || {}).length;
        const edgeCount = (data.edges || []).length;
        updateInfoPanel(`Graphe chargé: ${nodeCount} nœuds, ${edgeCount} arêtes`);
        drawGraph();
    } catch (error) {
        showError('Erreur lors du chargement du graphe: ' + error.message);
        console.error('Erreur détaillée:', error);
    }
}

// Dessiner le graphe
function drawGraph() {
    if (!graphData || !graphData.nodes) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const nodes = graphData.nodes;
    const edges = graphData.edges || [];
    const nodePositions = {};

    // Calculer les positions des nœuds (si pas déjà définies, utiliser un cercle)
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(canvas.width, canvas.height) / 3;
    const nodeNames = Object.keys(nodes);
    const angleStep = (2 * Math.PI) / nodeNames.length;

    nodeNames.forEach((nodeName, index) => {
        const node = nodes[nodeName];
        // Si x=0 ET y=0, utiliser position automatique en cercle, sinon utiliser les coordonnées fournies
        let x, y;
        if (node.x === 0 && node.y === 0) {
            // Position automatique en cercle
            x = centerX + radius * Math.cos(index * angleStep);
            y = centerY + radius * Math.sin(index * angleStep);
        } else {
            // Utiliser les coordonnées de la base de données
            x = node.x !== undefined && node.x !== null ? node.x : centerX + radius * Math.cos(index * angleStep);
            y = node.y !== undefined && node.y !== null ? node.y : centerY + radius * Math.sin(index * angleStep);
        }
        
        nodePositions[nodeName] = { x, y };
    });

    // Dessiner les arêtes
    edges.forEach(edge => {
        const posA = nodePositions[edge.node_a];
        const posB = nodePositions[edge.node_b];
        
        if (posA && posB) {
            // Vérifier si cette arête fait partie du chemin Dijkstra
            const isInPath = dijkstraPath && (
                (dijkstraPath.includes(edge.node_a) && dijkstraPath.includes(edge.node_b) &&
                 Math.abs(dijkstraPath.indexOf(edge.node_a) - dijkstraPath.indexOf(edge.node_b)) === 1)
            );

            ctx.strokeStyle = isInPath ? '#28a745' : '#ccc';
            ctx.lineWidth = isInPath ? 3 : 1;
            ctx.setLineDash(isInPath ? [] : []);
            
            ctx.beginPath();
            ctx.moveTo(posA.x, posA.y);
            ctx.lineTo(posB.x, posB.y);
            ctx.stroke();

            // Dessiner le poids
            const midX = (posA.x + posB.x) / 2;
            const midY = (posA.y + posB.y) / 2;
            ctx.fillStyle = '#666';
            ctx.font = '12px Arial';
            ctx.fillText(edge.weight, midX + 5, midY - 5);
        }
    });

    // Dessiner les nœuds
    nodeNames.forEach(nodeName => {
        const pos = nodePositions[nodeName];
        const color = getNodeColor(nodeName);
        
        // Cercle du nœud
        ctx.beginPath();
        ctx.arc(pos.x, pos.y, 20, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.strokeStyle = '#333';
        ctx.lineWidth = 2;
        ctx.stroke();

        // Nom du nœud
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 14px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(nodeName, pos.x, pos.y);
    });
}

// Obtenir la couleur d'un nœud (coloriage ou défaut)
function getNodeColor(nodeName) {
    if (coloringData && coloringData[nodeName]) {
        const colorMap = {
            'rouge': '#dc3545',
            'bleu': '#007bff',
            'vert': '#28a745',
            'jaune': '#ffc107',
            'violet': '#6f42c1',
            'orange': '#fd7e14',
            'rose': '#e83e8c',
            'cyan': '#17a2b8'
        };
        return colorMap[coloringData[nodeName]] || '#667eea';
    }
    return '#667eea';
}

// Appliquer le coloriage
async function applyColoring() {
    try {
        const response = await fetch(`${API_BASE_URL}/algo/coloring`);
        const data = await response.json();
        coloringData = {};
        
        // Convertir la liste en dictionnaire
        if (Array.isArray(data)) {
            data.forEach(item => {
                coloringData[item.node] = item.color;
            });
        } else {
            coloringData = data;
        }

        const resultBox = document.getElementById('coloring-result');
        resultBox.className = 'result-box show success';
        resultBox.innerHTML = '<h3>Coloriage appliqué</h3>';
        
        const colorList = Array.isArray(data) ? data : Object.entries(data).map(([node, color]) => ({ node, color }));
        colorList.forEach(item => {
            const colorDiv = document.createElement('div');
            colorDiv.className = 'color-item';
            colorDiv.style.backgroundColor = getNodeColor(item.node);
            colorDiv.textContent = `${item.node}: ${item.color}`;
            resultBox.appendChild(colorDiv);
        });

        drawGraph();
    } catch (error) {
        showError('Erreur lors du coloriage: ' + error.message);
    }
}

// Calculer le chemin avec Dijkstra
async function calculateDijkstra(e) {
    e.preventDefault();
    const source = document.getElementById('dijkstra-source').value || 'Depot';
    const target = document.getElementById('dijkstra-target').value;

    if (!target) {
        showError('Veuillez spécifier un nœud cible');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/algo/dijkstra?source=${encodeURIComponent(source)}&target=${encodeURIComponent(target)}`);
        const data = await response.json();

        if (data.error) {
            const resultBox = document.getElementById('dijkstra-result');
            resultBox.className = 'result-box show error';
            resultBox.innerHTML = `<h3>Erreur</h3><p>${data.error}</p>`;
            dijkstraPath = null;
        } else {
            dijkstraPath = data.path || [];
            const resultBox = document.getElementById('dijkstra-result');
            resultBox.className = 'result-box show success';
            resultBox.innerHTML = `
                <h3>Chemin trouvé</h3>
                <div class="distance">Distance: ${data.distance}</div>
                <div class="path">Chemin: ${dijkstraPath.join(' → ')}</div>
            `;
            updateInfoPanel(`Chemin de ${source} à ${target}: ${data.distance} unités`);
        }

        drawGraph();
    } catch (error) {
        showError('Erreur lors du calcul de Dijkstra: ' + error.message);
    }
}

// Ajouter un nœud
async function addNode(e) {
    e.preventDefault();
    const name = document.getElementById('node-name').value;
    const x = parseInt(document.getElementById('node-x').value) || 0;
    const y = parseInt(document.getElementById('node-y').value) || 0;

    try {
        const response = await fetch(`${API_BASE_URL}/graph/node`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, x, y })
        });

        if (response.ok) {
            document.getElementById('node-name').value = '';
            document.getElementById('node-x').value = '0';
            document.getElementById('node-y').value = '0';
            await loadGraph();
            updateInfoPanel(`Nœud "${name}" ajouté à (${x}, ${y})`);
        } else {
            const data = await response.json();
            showError(data.error || 'Erreur lors de l\'ajout du nœud');
        }
    } catch (error) {
        showError('Erreur: ' + error.message);
    }
}

// Ajouter une arête
async function addEdge(e) {
    e.preventDefault();
    const nodeA = document.getElementById('edge-node-a').value;
    const nodeB = document.getElementById('edge-node-b').value;
    const weight = parseInt(document.getElementById('edge-weight').value);

    try {
        const response = await fetch(`${API_BASE_URL}/graph/edge`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ node_a: nodeA, node_b: nodeB, weight })
        });

        if (response.ok) {
            document.getElementById('edge-node-a').value = '';
            document.getElementById('edge-node-b').value = '';
            document.getElementById('edge-weight').value = '1';
            await loadGraph();
            updateInfoPanel(`Arête entre "${nodeA}" et "${nodeB}" ajoutée`);
        } else {
            const data = await response.json();
            showError(data.error || 'Erreur lors de l\'ajout de l\'arête');
        }
    } catch (error) {
        showError('Erreur: ' + error.message);
    }
}

// Ajouter une contrainte
async function addConstraint(e) {
    e.preventDefault();
    const nodeA = document.getElementById('constraint-node-a').value;
    const nodeB = document.getElementById('constraint-node-b').value;
    const penalty = parseFloat(document.getElementById('constraint-penalty').value);

    try {
        const response = await fetch(`${API_BASE_URL}/graph/constraint`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ node_a: nodeA, node_b: nodeB, penalty })
        });

        const resultBox = document.getElementById('constraint-result');
        
        if (response.ok) {
            const data = await response.json();
            document.getElementById('constraint-node-a').value = '';
            document.getElementById('constraint-node-b').value = '';
            document.getElementById('constraint-penalty').value = '0';
            resultBox.className = 'result-box show success';
            resultBox.innerHTML = `<h3>Contrainte ajoutée</h3><p>Pénalité de ${penalty} ajoutée à l'arête entre "${nodeA}" et "${nodeB}"</p>`;
            await loadGraph();
            updateInfoPanel(`Contrainte ajoutée: pénalité de ${penalty} sur l'arête "${nodeA}" - "${nodeB}"`);
        } else {
            const data = await response.json();
            resultBox.className = 'result-box show error';
            resultBox.innerHTML = `<h3>Erreur</h3><p>${data.error || 'Erreur lors de l\'ajout de la contrainte'}</p>`;
            showError(data.error || 'Erreur lors de l\'ajout de la contrainte');
        }
    } catch (error) {
        const resultBox = document.getElementById('constraint-result');
        resultBox.className = 'result-box show error';
        resultBox.innerHTML = `<h3>Erreur</h3><p>${error.message}</p>`;
        showError('Erreur: ' + error.message);
    }
}

// Effacer la visualisation
function clearVisualization() {
    dijkstraPath = null;
    coloringData = null;
    document.getElementById('dijkstra-result').className = 'result-box';
    document.getElementById('coloring-result').className = 'result-box';
    drawGraph();
    updateInfoPanel('Visualisation effacée');
}

// Mettre à jour le panneau d'information
function updateInfoPanel(message) {
    const infoPanel = document.getElementById('info-panel');
    infoPanel.innerHTML = `<p>${message}</p>`;
}

// Afficher une erreur
function showError(message) {
    updateInfoPanel(`❌ ${message}`);
    console.error(message);
}

