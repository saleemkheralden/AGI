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
        {'id': 1, "name": "Discrete Mathematics", "level": 0},
    ],
    'links': [],
}

$(document).ready(function () {

    socket = io("127.0.0.1:5000")

    socket.on("connect", () => {
        socket.emit("client-connect", {"msg": "hello"})
    })

    socket.on("hello", (args) => {
        console.log(args);
        // alert("OKOK");
    })

    socket.on("add-node", (args) => {
        console.log(args);
    })

    let graph_div = document.getElementById('graph');
    let width = graph_div.clientWidth, height = graph_div.clientHeight;

    // let svg = d3.select("#graph")
    //     .append("svg")
    //     .style("width", "100%")
    //     .style("height", "100%")
    //     .style("background-color", "transparent")




});