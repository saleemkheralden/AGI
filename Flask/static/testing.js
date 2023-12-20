const node_radius = 10, node_radius_h = 15,
    duration_ = 100, nodes_opacity_ = 1, nodes_opacity_h = 0.1,
    strength = -5e2, edge_strength=0.3, stroke_width = 2,
    zoom_in=5, zoom_out=0.5, node_color="red",
    edge_color="cornflowerblue", font_size="12px",
    max_distance=250

const node_index = {}
const node_keys = new Set()

let socket;
let svg, simulation;

const data_ids = {
    'nodes': [],
    'links': [],
}

const links_q = [];

const data = {
    'nodes': [
        // {'id': 1, "label": "Discrete Mathematics", "str_score": 1},
        // {'id': 2, "label": "Calculus 1", "str_score": 1},
        // {'id': 3, "label": "Algebra", "str_score": 1},
        // {'id': "0004", "label": "Intro to comp. sc.", "str_score": .5},
        // {'id': 5, "label": "Physics 1", "str_score": 1},
        //
        // {'id': 6, "label": "Into to Data science", "str_score": 1},
        // {'id': 7, "label": "Software eng.", "str_score": 1},
        // {'id': 8, "label": "Computer arch. and OS", "str_score": 1},
        // {'id': 9, "label": "Probability", "str_score": 1},
        // {'id': 10, "label": "Calculus 2", "str_score": 1},
    ],
    'links': [
        // {"source": 1, "target": 2, "str_score": .5},
        // {"id": 1, "source": 6, "target": "0004", "str_score": .8},
        // {"id": 2, "source": 6, "target": 3, "str_score": .7},
        // {"id": 3, "source": 7, "target": "0004", "str_score": 1},
        // {"id": 4, "source": 8, "target": "0004", "str_score": .1},
        // {"id": 5, "source": 9, "target": 2, "str_score": 1},
        // {"id": 6, "source": 10, "target": 2, "str_score": 1},
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
        if (!data_ids.nodes.includes(args.id)) {
            data_ids.nodes.push(args.id)
            data.nodes.push(args);
            update();
        }
    })

    socket.on("add-edge", (args) => {
        console.log(args);
        if (!data_ids.links.includes(args.id)) {
            data_ids.links.push(args.id);

            let edge_json = {
                "id": args.id,
                "source": args.source.id,
                "target": args.target.id,
                "str_score": args.str_score,
            }
            console.log(edge_json)

            links_q.push(edge_json);
        }
    })

    socket.on("add-test-edge", (args) => {
        console.log(args);
        if (!data_ids.links.includes(args.id)) {
            data_ids.links.push(args.id);
            links_q.push(args);
        }
    })

    setInterval(() => {
        if (simulation.alpha() < 0.001)
            if (links_q.length > 0) {
                console.log("from set interval");
                console.log(simulation.alpha())
                data.links.push(links_q.pop())
                update()
            }
    }, 100)


    let graph_div = document.getElementById('graph');
    let width = graph_div.clientWidth, height = graph_div.clientHeight;

    let zoom_simulation = d3.zoom()
        .scaleExtent([zoom_out, zoom_in])
        .on("zoom", zoomed);

    svg = d3.select("#graph")
        .append("svg")
        .style("width", "100%")
        .style("height", "100%")
        .style("background-color", "transparent")
        .call(zoom_simulation)

    svg = svg.append("g")
        .attr("class", "zoom-layer")
        .attr("id", "zoom-layer")

    function zoomed() {
        svg.attr("transform", d3.event.transform);
    }


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
        // Add nodes
        let nodes_container = svg.select("g.nodes")
            .selectAll("g")
            .data(data.nodes)

        let nodes_container_enter = nodes_container.enter()
            .append("g")


        nodes_container_enter
            .append("circle")
            .attr("r", node_radius)
            .attr("fill", node_color)
            .attr("opacity", d => d.str_score)

        nodes_container_enter.append("text")
            .text(d => d.label)
            .attr("x", node_radius)
            .attr("y", ".35em")
            .attr("font-size", font_size)
            .attr("fill", "black")
            .style("pointer-event", "none")


        nodes_container.exit().remove();

        // Add links
        let links = svg.select("g.links")
            .selectAll("line")
            .data(data.links)

        let links_enter = links.enter()
            .append("line")

        links_enter.attr("stroke", edge_color)
            .attr("opacity", d => d.str_score)

        console.log(links_enter);

        links.exit().remove();



        simulation = d3.forceSimulation(data.nodes) // <- this is another way to run the simulation
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
        .on("tick", ticked) // <- another way to run the simulation
        // .on("end", () => {
        //     if (links_q.length > 0) {
        //         console.log("ADDING EDGE")
        //         let edge = links_q.pop();
        //         console.log(edge)
        //         data.links.push(edge);
        //         update();
        //     }
        // })

        nodes_container.call(drag(simulation));
        nodes_container_enter.call(drag(simulation));

        function ticked() {
            nodes_container
                .attr("transform", function(d) {
                    return "translate(" + d.x + ", " + d.y + ")";
                })

            nodes_container_enter
                .attr("transform", function(d) {
                    return "translate(" + d.x + ", " + d.y + ")";
                })

            links
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });


            links_enter
                .attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

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