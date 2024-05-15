///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// inits
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function init_inits(el) {
    let component_name = el.__liveflask['class']
    //el.__liveflask['children'] = attr_beginswith('data-component', el);
    let retrieved_inits = attr_beginswith('data-init', el);
    el.__liveflask['inits'] = [];
    let current_component;

    retrieved_inits.forEach(i => {
        current_component = i.parentNode.closest('[data-component]').getAttribute("data-component");
        if (current_component !== component_name) return;
        el.__liveflask['inits'].push(i)
    })


    el.__liveflask['inits'].forEach((i, index) => {
        let property;
        let value;
        let modifier;


        [property, modifier, value] = get_model_prop_value(i, "data-init")

        let method = property.split("(")[0];
        let args;
        try {
            args = replace_undefined(property).match(/\(([^)]+)\)/)[1];
            // Love this one console.log(args)
        } catch (e) {
            args = "__NOVAL__"
        }

        send_request(el, {'method': method, "args": args}, i)
    })

}
