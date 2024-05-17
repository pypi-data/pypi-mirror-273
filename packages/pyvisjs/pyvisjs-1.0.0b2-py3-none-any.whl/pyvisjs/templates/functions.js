
// converts ["edge,country,LV","edge,country,GB"]
// to
// {country: {list: ["LV", "GB"], type="edge"}}
function convert_field_value_list_to_dict(list) {
    dict = {}
    for (id in list) {
        const field_value_triplet = list[id].split(",")
        const type = field_value_triplet[0]
        const field = field_value_triplet[1]
        const value = field_value_triplet[2]

        if (field in dict) dict[field]["list"].push(value)
        else dict[field] = {"list": [value], "type": type}
    }
    return dict
}

function get_nodes_by_edge_attribute_value(field, value) {

    const result = [];

    for (const key in data.edges) {
        const edge = data.edges[key];

        if (edge[field] === value)
        {
            if (result.includes(edge.from) === false) result.push(edge.from);
            if (result.includes(edge.to) === false) result.push(edge.to);
        }
    }

    return result;
}

function find_node_by_attribute_value(field, value) {

    for (const key in data.nodes) {
        const node = data.nodes[key];

        if (node[field] === value)
        {
            return node["id"];
        }
    }

    return null;
}

function hide_nodes_by_edge_attribute_values_intersect(option_groups_dict) {

    const selected_nodes_by_field = {}

    for (field in option_groups_dict) {
        const dict = option_groups_dict[field]
        const selected_values = dict["list"]
        const node_or_edge = dict["type"]
        selected_nodes_by_field[field] = []

        for (id in selected_values) {
            let collected_nodes = []
            const value = selected_values[id];

            if (node_or_edge === "ALL" && value === "ALL") {
                collected_nodes = Object.keys(data.nodes);
                data.network.has_hidden_nodes = false;
            }
            else if (node_or_edge === "edge") {
                collected_nodes = get_nodes_by_edge_attribute_value(field, value)
                data.network.has_hidden_nodes = true;
            }
            else if (node_or_edge === "node") {
                const selected_node = find_node_by_attribute_value(field, value);
                collected_nodes = data.network.getConnectedNodes(selected_node);
                collected_nodes.push(selected_node);
                data.network.has_hidden_nodes = true;
            }

            for (id in collected_nodes) {
                node_id = collected_nodes[id]
                if (selected_nodes_by_field[field].includes(node_id) === false) selected_nodes_by_field[field].push(node_id)
            }
        }
    }

    const selected_nodes_intersection = apply_intersect(selected_nodes_by_field);
    changed_nodes = toggle_nodes(selected_nodes_intersection);

    data.ds_nodes.update(changed_nodes)
}

function apply_intersect(nodes_by_field_dict) {
    let field_with_shortest_list = null
    let min_list_len = 100000;

    //if nodes_by_field_dict is empty dict - return empty list
    if (nodes_by_field_dict === null || Object.keys(nodes_by_field_dict).length === 0) {
        return [];
    }

    //if nodes_by_field_dict contains only one field - just return values
    if (nodes_by_field_dict.length === 1) {
        return nodes_by_field_dict[0];
    }

    // find shortest list
    for (field_name in nodes_by_field_dict) {
        const curr_list_len = nodes_by_field_dict[field_name].length
        if (curr_list_len < min_list_len) {
            field_with_shortest_list = field_name
            min_list_len = curr_list_len
        }
    }

    // we start from the list of all node ids from the shortest list
    // our goal is to reduce it by compariong with other lists
    let intersection = nodes_by_field_dict[field_with_shortest_list]

    // pairwise comparison
    for (field_name in nodes_by_field_dict) {
        if (field_name !== field_with_shortest_list) {
            const nodes_list = nodes_by_field_dict[field_name];
            intersection = intersection.filter((node_id) => nodes_list.includes(node_id))
        }
    }

    return intersection;
}

function hide_nodes_by_edge_attribute_values_union(option_groups_dict) {

    const selectedNodes = [];

    for (field in option_groups_dict) {
        const dict = option_groups_dict[field]
        const selected_values = dict["list"]
        const node_or_edge = dict["type"]

        for (id in selected_values) {
            let collected_nodes = []
            const value = selected_values[id];

            if (node_or_edge === "ALL" && value === "ALL") {
                collected_nodes = Object.keys(data.nodes);
                data.network.has_hidden_nodes = false;
            }
            else if (node_or_edge === "edge") {
                collected_nodes = get_nodes_by_edge_attribute_value(field, value)
                data.network.has_hidden_nodes = true;
            }
            else if (node_or_edge === "node") {
                const selected_node = find_node_by_attribute_value(field, value);
                collected_nodes = data.network.getConnectedNodes(selected_node);
                collected_nodes.push(selected_node);
                data.network.has_hidden_nodes = true;
            }

            for (id in collected_nodes) {
                node_value = collected_nodes[id]
                if (selectedNodes.includes(node_value) === false) selectedNodes.push(node_value)
            }
        }
    }

    changed_nodes = toggle_nodes(selectedNodes);

    data.ds_nodes.update(changed_nodes)
}

function hide_not_selected_nodes(event) {
    // has selected nodes or already has hidden nodes - in both cases we have work to do
    if (event.nodes.length > 0 || data.network.has_hidden_nodes === true) {
        let selectedNodes;
        
        // user clicked outside the nodes network - we want to unhide all the nodes
        if (event.nodes.length == 0 && data.network.has_hidden_nodes === true) {
            selectedNodes = Object.keys(data.nodes);
            data.network.has_hidden_nodes = false;
        }
        else {
            const selectedNode = event.nodes[0];
            selectedNodes = data.network.getConnectedNodes(selectedNode);
            selectedNodes.push(selectedNode);
            data.network.has_hidden_nodes = true;
        }

        changed_nodes = toggle_nodes(selectedNodes);

        //reset_all_filters(data.pyvisjs.edge_filtering_fields)
        data.ds_nodes.update(changed_nodes)
    }
}

function toggle_nodes(selectedNodes) {
    const changed_nodes = [];
    
    for (const key in data.nodes) {
        const node = data.nodes[key];
        const node_id = node["id"];
        // node is not hidden by default
        if (node.hasOwnProperty("_hidden") === false) node._hidden = false;
        
        // nodes to hide
        if (selectedNodes.includes(node_id) === false)
        {
            // not already hidden
            if (node._hidden === false)
            {
                node._hidden = true;
                if (data.pyvisjs.enable_highlighting === false) node.hidden = true;
                node._color = node.color;
                node.color = "rgba(200,200,200,0.5)";
                changed_nodes.push(node)
            }
        }
        // nodes to unhide (only if already hidden)
        else if (node._hidden === true) {
            node._hidden = false;
            if (data.pyvisjs.enable_highlighting === false) node.hidden = false;
            node.color = node._color ? node._color : "#97C2FC";
            node._color = undefined;
            changed_nodes.push(node)
        }
    }

    return changed_nodes
}