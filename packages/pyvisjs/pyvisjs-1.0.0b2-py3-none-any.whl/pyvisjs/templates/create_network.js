const data = create_network();
data.network.has_hidden_nodes = false;
//if (data.pyvisjs.enable_highlighting === true) data.network.on("click", hide_not_selected_nodes);

// all jinja injections should happen here because it allows to mock this function and test all the rest in isolation
function create_network() {

    // create an array with nodes
    const ds_nodes = new vis.DataSet({{ data["nodes"]|tojson }});

    // create an array with edges
    const ds_edges = new vis.DataSet({{ data["edges"]|tojson }});

    // create a network
    const container = document.getElementById('visjsnet');

    // provide the data in the vis format
    const data = {
        nodes: ds_nodes,
        edges: ds_edges
    };
    const options = {{ data["options"]|tojson }};
    const pyvisjs = {{ pyvisjs|tojson }};

    return {
        network: new vis.Network(container, data, options),
        nodes: ds_nodes.get({ returnType: "Object" }),
        edges: ds_edges.get({ returnType: "Object" }),
        ds_nodes: ds_nodes,
        pyvisjs: pyvisjs,
    }
}