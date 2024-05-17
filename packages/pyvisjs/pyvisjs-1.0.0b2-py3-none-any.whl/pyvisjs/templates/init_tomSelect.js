const eventHandler = function(name) {
    return function() {
        const list_of_selected_values = arguments[0]
        dict = convert_field_value_list_to_dict(list_of_selected_values)
        hide_nodes_by_edge_attribute_values_intersect(dict)
    };
};

new TomSelect("#select-all-fields", {
    maxItems: 10,
    onChange: eventHandler("onChange"),
    //create: true,
    //onItemAdd:function(){
    //    this.setTextboxValue('');
    //    this.refreshOptions();
    //},
    plugins: ['remove_button'],
});