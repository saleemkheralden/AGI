const node_radius = 10, node_radius_h = 15,
    duration_ = 100, nodes_opacity_ = 1, nodes_opacity_h = 0.1,
    strength = -5e2, edge_strength=0.3, stroke_width = 2,
    zoom_in=5, zoom_out=0.5, node_color="red",
    edge_color="cornflowerblue", font_size="12px",
    max_distance=250

const node_index = {}
const node_keys = new Set()

$(document).ready(function () {
    let graph_div = document.getElementById('graph');
    let width = graph_div.clientWidth, height = graph_div.clientHeight;


    const data = {
        'nodes': [
            {'id': 1, "name": "Discrete Mathematics", "level": 0},
            {'id': 2, "name": "Calculus 1", "level": 0},
            {'id': 3, "name": "Algebra", "level": 0},
            {'id': 4, "name": "Intro to comp. sc.", "level": 0},
            {'id': 5, "name": "Physics 1", "level": 0},

            {'id': 6, "name": "Into to Data science", "level": 1},
            {'id': 7, "name": "Software eng.", "level": 1},
            {'id': 8, "name": "Computer arch. and OS", "level": 1},
            {'id': 9, "name": "Probability", "level": 1},
            {'id': 10, "name": "Calculus 2", "level": 1},

            {'id': 11, "name": "Game theory", "level": 2},
            {'id': 12, "name": "Data structures", "level": 2},
            {'id': 13, "name": "Databases", "level": 2},
            {'id': 14, "name": "Algebra for data science", "level": 2},
            {'id': 15, "name": "Statistics 1", "level": 2},

            {'id': 16, "name": "Stochastic models", "level": 3},
            {'id': 17, "name": "E-comm", "level": 3},
            {'id': 18, "name": "Distributed DBs", "level": 3},
            {'id': 19, "name": "Non-linear models", "level": 3},
            {'id': 20, "name": "Into to complexity", "level": 3},
            {'id': 21, "name": "Machine Learning 1", "level": 3},

            // {'id': 21, "name": "Machine Learning 1", "level": 4},

        ],
        'links': [
            {"source": 6, "target": 4, "weight": 1},
            {"source": 6, "target": 3, "weight": 1},
            {"source": 7, "target": 4, "weight": 1},
            {"source": 8, "target": 4, "weight": 1},
            {"source": 9, "target": 2, "weight": 1},
            {"source": 10, "target": 2, "weight": 1},

            {"source": 11, "target": 2, "weight": 1},
            {"source": 11, "target": 3, "weight": 1},
            {"source": 12, "target": 1, "weight": 0.5},
            {"source": 12, "target": 7, "weight": 1},
            {"source": 13, "target": 1, "weight": 0.5},
            {"source": 13, "target": 4, "weight": 1},
            {"source": 14, "target": 1, "weight": 1},
            {"source": 14, "target": 2, "weight": 1},
            {"source": 14, "target": 3, "weight": 1},
            {"source": 14, "target": 4, "weight": 1},
            {"source": 15, "target": 9, "weight": 1},

            {"source": 16, "target": 9, "weight": 1},
            {"source": 16, "target": 3, "weight": 1},
            {"source": 16, "target": 4, "weight": 1},
            {"source": 17, "target": 12, "weight": 1},
            {"source": 17, "target": 9, "weight": 1},
            {"source": 18, "target": 13, "weight": 1},
            {"source": 19, "target": 10, "weight": 1},
            {"source": 20, "target": 12, "weight": 1},
            {"source": 21, "target": 15, "weight": 1},
            {"source": 21, "target": 4, "weight": 1},

        ]
    }


    let zoom = d3.zoom()
        .scaleExtent([zoom_out, zoom_in])
        .on("zoom", zoomed);

    let svg = d3.select("#graph")
        .append("svg")
        .style("width", "100%")
        .style("height", "100%")
        .style("background-color", "transparent")
        .call(zoom);

    let zoom_elem = svg.append("g")
        .attr("class", "zoom-layer")
        .attr("id", "zoom-layer")

    function zoomed() {
        // console.log(d3.event);
        zoom_elem.attr("transform", d3.event.transform);
    }

    let simulation = d3.forceSimulation()
        .force("link", d3.forceLink().id(d => d.id).strength(edge_strength))
        .force("charge",
            d3.forceManyBody().strength(strength)
                .distanceMax([max_distance]))
        .force("center", d3.forceCenter(width / 2, height / 2));

    let link = zoom_elem.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .attr("stroke", edge_color)
        .attr("opacity", function (d) {
            return d.weight
        })
        .attr("stroke-width", stroke_width);

    let textsAndNodes = zoom_elem.append("g")
        .selectAll("g")
        .data(data.nodes)
        .enter()
        .append("g")
        .attr("class", "textsAndNodes")
        .call(drag(simulation))

    // let fixednode = d3.select("1").attr("fixed", true)

    let nodes = textsAndNodes
        .append("a")
        // .attr("href", function (d) {return d.name})
        .append("circle")
        .attr("r", node_radius)
        // .attr("fill", node_color)
        // .attr("fill", "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg")
        .on("mouseover", function (d) {
            show_nodes(d, this);
        })
        .on("mouseout", function (d) {
            d3.selectAll("circle").style("opacity", nodes_opacity_);
            d3.selectAll("line").style("opacity", nodes_opacity_)
            d3.selectAll("text").style("opacity", nodes_opacity_)

            d3.select(this)
                .transition()
                .duration(duration_)
                .attr("r", node_radius);
        })

    let images = textsAndNodes.append("image")
            .attr("xlink:href", function (d) { return "https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg" })
            .attr("x", "-25px")
            .attr("y", "0")
            .attr("height", "50px")
            .attr("width", "50px")

    let texts = textsAndNodes.append("text")
        .text(function (d) {
            return d.name;
        })
        .attr("x", node_radius)
        .attr("y", ".35em")
        .attr("font-size", font_size)
        .attr("fill", "black")
        .style("pointer-events", "none")


    simulation
        .nodes(data.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(data.links);

    function calcy(lower, upper, y) {
        function min(a, b) { return a < b ? a : b}
        function max(a, b) { return a > b ? a : b}


        return max(min(y, upper), lower)
    }

    function ticked() {
        // fixednode
        //     .attr("cx", function(d) { return d.x; })
        //     .attr("cy", function(d) { return d.y; });

        link
            .attr("x1", function (d) {
                return d.source.x;
            })
            .attr("y1", function (d) {
                return d.source.y;
                // return 200 * d.source.level;
                // return calcy(200 * d.source.level - 50, 200 * d.source.level + 50, 200 * d.source.level);
            })
            .attr("x2", function (d) {
                return d.target.x;
            })
            .attr("y2", function (d) {
                return d.target.y;
                // return 200 * d.target.level;
                // return calcy(200 * d.target.level - 50, 200 * d.target.level + 50, 200 * d.target.level);
            });

        textsAndNodes.attr("transform", function (d) {
            update_index(d);
            return "translate(" + d.x + ", " + d.y + ")"
            // return "translate(" + d.x + ", " + 200 * d.level + ")"
            // return "translate(" + d.x + ", " + calcy(200 * d.level - 50, 200 * d.level + 50, 200 * d.level) + ")"
        });
        // fixednode
        //   .attr("cx", function(d) { return d.x; })
        //   .attr("cy", function(d) { return d.y; });
    }

    function drag(simulation) {
        function dragstarted(event) {
            // console.log(event);
            // console.log(d3.event);
            if (!d3.event.active) simulation.alphaTarget(0.3).restart();
            event.fx = d3.event.x;
            event.fy = d3.event.y;

            update_index(event);
        }

        function dragged(event) {

            show_nodes(event, this);

            event.fx = d3.event.x;
            event.fy = d3.event.y;

            update_index(event);
        }

        function dragended(event) {
            if (!event.active) simulation.alphaTarget(0);
            event.fx = null;
            event.fy = null;

            update_index(event);

            d3.selectAll("circle").style("opacity", 1);
            d3.select(this)
                .transition()
                .duration(duration_)
                .attr("r", node_radius);
        }

        return d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended);
    }

    function show_nodes(e, this_e) {
        d3.selectAll("circle")
            .transition()
            .duration(duration_)
            .style("opacity", nodes_opacity_h)

        d3.selectAll("line")
            .transition()
            .duration(duration_)
            .style("opacity", nodes_opacity_h)

        d3.selectAll("text")
            .transition()
            .duration(duration_)
            .style("opacity", nodes_opacity_h)

        d3.selectAll("text")
            .filter(node =>
                data.links.some(
                    link =>
                        (link.source.id === e.id ||
                            link.target.id === e.id) &&
                        (link.source.id === node.id ||
                            link.target.id === node.id)))
            .transition()
            .style("opacity", nodes_opacity_)

        d3.selectAll("line")
            .filter(link =>
                data.nodes.some(
                    node =>
                        (link.source.id === e.id ||
                            link.target.id === e.id) &&
                        (link.source.id === node.id ||
                            link.target.id === node.id)))
            .transition()
            .style("opacity", nodes_opacity_)

        d3.selectAll("circle")
            .filter(node =>
                data.links.some(
                    link =>
                        (link.source.id === e.id ||
                            link.target.id === e.id) &&
                        (link.source.id === node.id ||
                            link.target.id === node.id)))
            .transition()
            .style("opacity", nodes_opacity_)

        d3.select(this_e)
            .transition()
            .duration(duration_)
            .attr("r", node_radius_h)


        // this selects the connected nodes except d
        // let connectedNodes = data.links
        //     .filter(link => link.source.id === d.id || link.target.id === d.id)
        //     .map(link => link.source.id === d.id ? link.target : link.source);

        // d3.selectAll("circle")
        //     .filter(node =>
        //         connectedNodes.some(
        //             connectedNode =>
        //                 connectedNode.id === node.id))

    }

    function update_index(e) {
        node_index[e.name] = {'id': e.id, 'coor': [e.x, e.y]};
        node_keys.add(e.name);
    }

});


