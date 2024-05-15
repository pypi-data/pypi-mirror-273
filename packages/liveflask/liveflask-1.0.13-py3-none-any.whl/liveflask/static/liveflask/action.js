///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// ACTIONS & EVENTS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function init_action(el) {
    let component_name = el.__liveflask['class']
    let retrieved_actions = attr_beginswith('live-action', el);
    //console.log(retrieved_actions)
    el.__liveflask['actions'] = [];
    el.__liveflask.prefetches = [];
    let current_component;

    retrieved_actions.forEach(i => {
        current_component = i.parentNode.closest('[live-component]').getAttribute("live-component");
        if (current_component !== component_name) return;
        el.__liveflask['actions'].push(i)
    })

    function handle_action(property, el, i) { // Added 'property' as a parameter
        // Split property into method and arguments
        let method = property.split("(")[0].trim(); // Added .trim() to remove leading/trailing spaces
        let args;
        try {
            // Fixed 'replace_undefined' to properly handle undefined property
            args = property.match(/\(([^)]+)\)/)[1].trim(); // Removed replace_undefined and trimmed whitespace
            // Love this one console.log(args)
        } catch (e) {
            args = "__NOVAL__";
        }

        if (i.hasAttribute('live-action-confirm')) {
            if (confirm(i.getAttribute("live-action-confirm"))) {
                // Fixed sending arguments as string, ensuring it's an array
                send_request(el, {'method': method, "args": args}, i); // Split args into array
            } else {
                return false;
            }

        } else if (i.hasAttribute('live-action-confirm-prompt')) {
            let prompt_message = i.getAttribute("live-action-confirm-prompt");
            let accepted_value = prompt_message.split("|")[1].trim();
            let prompt_response = prompt(prompt_message.split("|")[0].trim());

            if (accepted_value === prompt_response) {
                // Fixed sending arguments as string, ensuring it's an array
                send_request(el, {'method': method, "args": args}, i); // Split args into array
            } else {
                return false;
            }
        } else {
            // Fixed sending arguments as string, ensuring it's an array
            send_request(el, {'method': method, "args": args}, i); // Split args into array
        }
    }


    el.__liveflask['actions'].forEach(i => {
        let property;
        let value;
        let modifier;
        let action_event;


        [property, modifier, value] = get_model_prop_value(i, "live-action")

        if (!i.__data_action_click_registered) {
            i.addEventListener('click', event => {
                handle_action(property, el, i); // Added 'property' as a parameter
            })

            if (i.hasAttribute("live-action-mouseenter")) {
                i.addEventListener('mouseenter', event => {
                    handle_action(property, el, i); // Added 'property' as a parameter
                })
            }

            if (i.hasAttribute("live-action-keydown")) {
                let key = i.getAttribute("live-action-keydown");
                i.addEventListener('keydown', event => {
                    if (event.key === key) {
                        handle_action(property, el, i); // Added 'property' as a parameter
                    }
                })
            }

            if (i.hasAttribute("live-action-keyup")) {
                let key = i.getAttribute("live-action-keydown");
                i.addEventListener('keyup', event => {
                    if (event.key === key) {
                        handle_action(property, el, i); // Added 'property' as a parameter
                    }
                })
            }


            // if (i.hasAttribute("live-action-prefetch") && i.getAttribute("live-action-prefetch") === "true") {
            //     i.addEventListener('mouseover', event => {
            //         let method = property.split("(")[0];
            //         let args;
            //         try {
            //             args = replace_undefined(property).match(/\(([^)]+)\)/)[1];
            //             // Love this one console.log(args)
            //         } catch (e) {
            //             args = "__NOVAL__"
            //         }
            //         send_request(el, {'method': method, "args": args}, i, true)
            //     })
            // }

            i.__data_action_click_registered = true
        }
    })


}

