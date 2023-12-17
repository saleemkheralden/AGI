const node_radius = 10, node_radius_h = 15,
    duration_ = 100, nodes_opacity_ = 1, nodes_opacity_h = 0.1,
    strength = -5e2, edge_strength=0.3, stroke_width = 2,
    zoom_in=5, zoom_out=0.5, node_color="red",
    edge_color="cornflowerblue", font_size="12px",
    max_distance=250

const node_index = {}
const node_keys = new Set()

let socket;
const data = {
    'nodes': [
        {'id': 1, "label": "Discrete Mathematics"},
        {'id': 2, "label": "Calculus 1"},
        {'id': 3, "label": "Algebra"},
        {'id': 4, "label": "Intro to comp. sc."},
        {'id': 5, "label": "Physics 1"},

        {'id': 6, "label": "Into to Data science"},
        {'id': 7, "label": "Software eng."},
        {'id': 8, "label": "Computer arch. and OS"},
        {'id': 9, "label": "Probability"},
        {'id': 10, "label": "Calculus 2"},
    ],
    'links': [
        {"source": 1, "target": 2, "weight": 1},
        {"source": 6, "target": 4, "weight": 1},
        {"source": 6, "target": 3, "weight": 1},
        {"source": 7, "target": 4, "weight": 1},
        {"source": 8, "target": 4, "weight": 1},
        {"source": 9, "target": 2, "weight": 1},
        {"source": 10, "target": 2, "weight": 1},
    ],
}

$(document).ready(function () {

    socket = io("127.0.0.1:5000")

    socket.on("connect", () => {
        socket.emit("client-connect", {"msg": "hello"})
    })

    socket.on("hello", (args) => {
        console.log(args);
    })

    socket.on("add-node", (args) => {
        console.log(args);
        data.nodes.push(args);
        update();
    })

    let graph_div = document.getElementById('graph');
    let width = graph_div.clientWidth, height = graph_div.clientHeight;

    let svg = d3.select("#graph")
        .append("svg")
        .style("width", "100%")
        .style("height", "100%")
        .style("background-color", "transparent")

    svg.append("g")
        .attr("class", "links")
    svg.append("g")
        .attr("class", "nodes")

    function drag(simulation) {
        function dragstarted(event) {
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            event.fx = d3.event.x;
            event.fy = d3.event.y;
        }

        function dragged(event) {
            event.fx = d3.event.x;
            event.fy = d3.event.y;
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.fx = null;
            event.fy = null;
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)

    }


    function update() {
        let links = svg.select("g.links")
            .selectAll("line")
            .data(data.links)
            .enter()
            .append("line")
            .attr("stroke", edge_color)

        links.exit().remove();

        let nodes_container = svg.select("g.nodes")
            .selectAll("g")
            .data(data.nodes)
            .enter()
            .append("g")

        nodes_container
            .append("circle")
            .attr("r", node_radius)
            .attr("fill", node_color)

        nodes_container.append("text")
            .text(d => d.label)
            .attr("x", node_radius)
            .attr("y", ".35em")
            .attr("font-size", font_size)
            .attr("fill", "black")
            .style("pointer-event", "none")


        nodes_container.exit().remove();

        let simulation = d3.forceSimulation(data.nodes) // <- this is another way to run the simulation
            .force("link",
                d3.forceLink()
                    .id(d => d.id)
                    .strength(edge_strength)
                    .links(data.links)) // <- this is another way to run the simulation
                                // This line adds a force to the simulation,
                                // specifically a link force.
                                // The link force simulates the links (edges) between nodes.
            .force("charge",
                d3.forceManyBody().strength(strength)
                    .distanceMax([max_distance]))
            // This line adds a many-body force to the simulation.
            // The many-body force simulates the forces between all pairs of nodes
            .force("center", d3.forceCenter(width / 2, height / 2))
            // This line adds a centering force to the simulation,
            // attracting nodes towards the center of the SVG container.
        .on("tick", ticked); // <- another way to run the simulation

        nodes_container.call(drag(simulation));

        function ticked() {
            links
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            nodes_container
                .attr("transform", function(d) {
                    return "translate(" + d.x + ", " + d.y + ")";
                })
                // .attr("cx", function(d) { return d.x; })
                // .attr("cy", function(d) { return d.y; });
        }

    }

    update();






    // another way to run the simulation is this lines of code below
    // if you apply this way, you can remove the data.nodes from the simulation.forceSimulation(data.nodes)
    // and you can remove the .links(data.links) from inside the .force("link", d3....links(data.links))

    // simulation.nodes(data.nodes)
    // .on("tick", ticked);

    // simulation.force("link").links(data.links)






});