    // Function to handle node search
function searchNode(groupIcons) {
    const searchTerm = document.getElementById("searchInput").value.toLowerCase();

    // Make an AJAX call to the Django view for searching by keywords
    fetch(`/search/by_keywords/${searchTerm}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json()) 
    .then(data => {
        // update visualization with data
        console.log("Server response:", data);
        nodes = data.nodes
        links = data.links
        document.querySelector("svg")?.remove()
        updateVisualization(nodes,links)
    })
    .catch(error => {
        console.error("Error:", error);
    });


    function updateVisualization(nodes = [], links=[]) {
        const containerWidth = window.innerWidth;
        const containerHeight = window.innerHeight;
        const svgWidth = containerWidth;
        const svgHeight = containerHeight;
        const centerX = svgWidth / 2;
        const centerY = svgHeight / 2;
        const radius = Math.min(svgWidth, svgHeight) * 0.4;
    
        const svg = d3.select("body")
            .append("svg")
            .attr("width", "100%")
            .attr("height", "100%")
            .attr("viewBox", `0 0 ${svgWidth} ${svgHeight}`)
            .attr("preserveAspectRatio", "xMidYMid meet")
            .append("g");
    
        window.addEventListener("resize", () => {
            // Update container size
            const containerWidth = window.innerWidth;
            const containerHeight = window.innerHeight;
    
            // Update SVG dimensions
            svg.attr("width", containerWidth)
            .attr("height", containerHeight);
        });
    
        function createLink(sourceId, targetId, relationshipType) {
            const sourceNode = nodes.find(node => node.id === sourceId);
            const targetNode = nodes.find(node => node.id === targetId);
    
            // Check if both source and target nodes are found before creating the link
            if (sourceNode && targetNode) {
                return {
                    source: sourceNode,
                    target: targetNode,
                    relationship_type: relationshipType
                };
            }
    
            // Handle the case where either source or target node is not found
            console.error(`Invalid link: Source or target node not found for relationship ${relationshipType}`);
            return null;
        }
        // icons mapping
        //groupIcon = {{ groupIcons|safe }}
    
        // initialize nodes:
        const angleStep = (2 * Math.PI) / nodes.length;
        nodes.forEach((node, index) => {
            node.x = centerX + radius * Math.cos(index * angleStep);
            node.y = centerY + radius * Math.sin(index * angleStep);
        });
    
        // Create a force simulation
        let width = window.innerWidth;
        let height = window.innerHeight
        const simulation = d3.forceSimulation(nodes)
            .force("link", d3.forceLink(links).id(d => d.id).strength(0.5)) // Increase link strength for more spacing
            .force("charge", d3.forceManyBody().strength(-1000).distanceMax(600))
            .force("collide", d3.forceCollide(35))
            //.force("center", d3.forceCenter(250, 150))
            .force("center", d3.forceCenter(width/2, height/2))
            ;
    
        // Draw relationships (lines)
        const link = svg.selectAll("line")
            .data(links)
            .enter().append("line")
            .attr("stroke-width", 2)
            .attr("stroke", "#ccc")
            .attr("data-edge-name", d => d.relationship_type)
            .attr("marker-end", "url(#arrowhead)");
    
            // Add arrowhead definition
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 5) // Adjust the refX value based on the length of your edges
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5") // Path for the arrowhead
            .attr("fill", "#ccc"); // Color of the arrowhead
    
        // Draw nodes (circles)       
        const node = svg.selectAll("circle")
            .data(nodes)
            .enter().append("g")
            .attr("r", 20)
            .call(d3.drag()
                .on("start", dragstarted)
                .on("drag", dragged)
                .on("end", dragended));
            
        node.append("image")
                .attr("class",function(d){
                    return d.type
                })
                .attr("xlink:href",function(d){
                    return groupIcons[d.type]
                })
                .attr("x",-15)
                .attr("y",-15)
                .attr("width",30)
                .attr("height",30);
    
        const nodeLabels = svg.selectAll(".node-label")
            .data(nodes)
            .enter().append("text")
            .attr("class", "node-label")
            .attr("dy", 5)
            .attr("text-anchor", "middle")
            .attr("fill", "white")
            .text(d => d.label)
            .style("font-size", "10px");
    
        // Draw edge names as text elements next to the links
        const edgeLabels = svg.selectAll(".edge-label")
            .data(links)
            .enter().append("text")
            .attr("class", "edge-label")
            .attr("text-anchor", "middle")
            .attr("fill", "black")
            .text(d => d.relationship_type)
            .style("font-size", "8px");
    
        // Add labels to nodes
        svg.selectAll("text")
            .data(nodes)
            .enter().append("text")
            .attr("dy", 5)
            .attr("text-anchor", "middle")
            .attr("fill", "white")
            .text(d => d.label);
    
        // Update node and link positions during simulation       
        simulation.on("tick", () => {
            link
                .attr("x1", d => d.source.x ?? 0) // Default to 0 if undefined
                .attr("y1", d => d.source.y ?? 0)
                .attr("x2", d => d.target.x ?? 0)
                .attr("y2", d => d.target.y ?? 0);
    
            node
                .attr("cx", d => d.x ?? 0)
                .attr("cy", d => d.y ?? 0)
                .attr("transform",d=>"translate("+d.x+","+d.y+")");
    
            // Update text positions for nodes
            nodeLabels
                .attr("x", d => (d.x ?? 0))
                .attr("y", d => (d.y ?? 0) + 25);
                
            // Update text positions
            svg.selectAll("text")
                .attr("x", d => (d.x ?? 0))
                .attr("y", d => (d.y ?? 0) + 25);
    
            edgeLabels
                .attr("x", d => (d.source.x + d.target.x) / 2 ?? 0)
                .attr("y", d => (d.source.y + d.target.y) / 2 ?? 0);
    
        });
                    
        // Drag functions
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
    
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
    
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }    

    }

}