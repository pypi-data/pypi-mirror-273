///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// UTILITIES
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

const MODIFIERS = [
    "defer",
    "lazy",
    "debounce"
];

const ATTRIBUTES = [
    "wire:model",
    "wire:poll",
    "wire:snapshot"
];

const print_ = console.log;


function createElementFromHTML(htmlString) {
    const parser = new DOMParser();
    const htmlDoc = parser.parseFromString(htmlString, 'text/xml');


    // Change this to div.childNodes to support multiple top-level nodes.
    return htmlDoc;
}

const attr_beginswith = (prefix, target, exclude_children = true) =>
    Array.from(target.querySelectorAll('*'))
        .filter(
            (e) => Array.from(e.attributes).filter(
                ({name, value}) => name.startsWith(prefix)).length
        );

function get_model_prop_value(el, attribute) {
    let property = el.getAttribute(attribute);
    let value = el.value;
    if (value === undefined) {
        value = el.innerHTML;
    }
    let modifier = "";
    if (property !== null) {

        if (property.split("|").length === 1) {

            return [property, modifier, value];
        }

        if (property.split("|").length === 2) {
            modifier = value.split("|")[0];
            value = value.split("|")[1];
            return [property, modifier, value];
        }
    }
}

const parse_model_attributes = el => {
    let property = el.getAttribute("live-model");
    return [];
};

function resolve(path, obj = self, separator = '.') {
    if (path.includes('undefined')) {
        path = path.split('.')[0];
    }
    let properties = Array.isArray(path) ? path : path.split(separator);
    let res = properties.reduce((prev, curr) => prev?.[curr], obj);
    if (typeof res === 'object') {
        return res[`${path.split('.')}`];
    } else {
        return res;
    }
}

function replace_undefined(item) {
    var str = JSON.stringify(item, function (key, value) {
            return (value === undefined || value.includes('.')) ? "" : value;
        }
    );
    return JSON.parse(str);
}

function parse_interval(str) {
    if (str === undefined) {
        return undefined;
    }
    if (str.slice(-2) === "ms") {
        return parseFloat(str.slice(0, -2)) || undefined;
    }
    if (str.slice(-1) === "s") {
        return (parseFloat(str.slice(0, -1)) * 1000) || undefined;
    }
    if (str.slice(-1) === "m") {
        return (parseFloat(str.slice(0, -1)) * 1000 * 60) || undefined;
    }
    return parseFloat(str) || undefined;
}

var debounce = (function () {
    var timers = {};

    return function (callback, delay, id) {
        delay = delay || 500;
        id = id || "duplicated event";

        if (timers[id]) {
            clearTimeout(timers[id]);
        }

        timers[id] = setTimeout(callback, delay);
    };
})(); // note the call here so the call for `func_to_param` is omitted


const debounceModel = _.debounce((el, payload) => {
    send_request(el, payload);
}, parse_interval('150ms'))


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// SERVER CALL
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function send_request(el, add_to_payload, target) {
    let updated_element;
    let emits;
    let snapshot = el.__liveflask
    let children = attr_beginswith('live-component', el);

    let elementsWithDataLoading = el.querySelectorAll('[live-loading]');
    let elementsWithDataAttr = el.querySelectorAll('[live-loading-attr]');

    elementsWithDataAttr.forEach(element => {
        let loading_attr = get_loading_attr(element);
        if (loading_attr !== undefined) {
            element.setAttribute(loading_attr, "true");
        }
    });

    elementsWithDataLoading.forEach(element => {
        let loading_classes = get_loading_class(element);

        if (element.hasAttribute("live-loading-target")) {
            let loading_target = element.getAttribute("live-loading-target");
            if (loading_target && loading_target.includes(',')) {
                loading_target = loading_target.split(',').map(item => item.trim());

                // Now loading_target is an array containing the split values
            } else {
                loading_target = [loading_target];
            }

            let target_action_or_model = target.getAttribute("live-action") || target.getAttribute("live-model");
            if (loading_target.includes(target_action_or_model)) {
                element.style.display = get_display_style(element);
                if (loading_classes !== undefined) {
                    loading_classes.forEach(loading_class => {
                        element.classList.add(loading_class);
                    });
                }
            }

        } else {
            element.style.display = "block";
            if (loading_classes !== undefined) {
                loading_classes.forEach(loading_class => {
                    element.classList.add(loading_class);
                });
            }
        }
    });

    fetch("/liveflask/", {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRF-Token": csrfToken},
        body: JSON.stringify({
            snapshot: snapshot,
            ...add_to_payload
        })
    }).then(response => {
        if (!response.ok) {
            if (response.status === 400) {
                return response.text().then(text => {
                    if (text.includes("The CSRF token has expired.")) {
                        // Handle CSRF token expiration here
                        onpageexpired();
                    } else {
                        throw new Error(text);
                    }
                });
            } else {
                throw new Error('Network response was not ok.');
            }
        }
        return response;
    }).then(i => i.json()).then(response => {
        let {html, snapshot} = response
        el.__liveflask = snapshot
        el.__liveflask['children'] = children

        if (target.hasAttribute("live-poll") === true) {
            morphdom(target, createElementFromHTML(html).querySelector(`[live-poll=${target.getAttribute('live-poll')}]`).outerHTML)
            return;
        }

        update_dom(el, html)

        let emits = el.__liveflask?.data?.emits;

        if (emits !== undefined) {
            /* loop through the emits and fire the events */
            Object.keys(emits).forEach(event => {
                let current_event = emits[event]
                let event_name = current_event['event']
                let event_params = current_event['params']
                let kwargs = current_event['kwargs']
                let to = current_event['to']
                let final_params = event_name
                document.dispatchEvent(new CustomEvent(event_name, {
                    detail: {
                        event: event_name,
                        params: event_params,
                        kwargs: kwargs,
                    }
                }));
                if (to === "self") {
                    send_request(el, {method: "emit", args: final_params, kwargs: kwargs}, target).then(() => {
                        // Update DOM synchronously after emitting events
                        update_dom(el, el.innerHTML);
                    });
                } else if (to === "all") {
                    let components = document.querySelectorAll(`[live-component]`)
                    components.forEach(component => {
                        send_request(component, {
                            method: "emit",
                            args: final_params,
                            kwargs: kwargs
                        }, target);
                    })
                } else {
                    let components = document.querySelectorAll(`[live-component=${to}]`)
                    components.forEach(component => {
                        send_request(component, {
                            method: "emit",
                            args: final_params,
                            kwargs: kwargs
                        }, target).then(() => {
                            // Update DOM synchronously after emitting events
                            update_dom(component, component.innerHTML);
                        });
                    })
                }

            })
        }

        // loop through el.__liveflask.data.url and update the page url with the new url
        let url_object = el.__liveflask?.data?.url;
        // url_object is a key-value pair object with key as the query parameter and value as the value
        if (url_object !== undefined) {
            let url = new URL(window.location.href);
            Object.keys(url_object).forEach(key => {
                url.searchParams.set(key, url_object[key]);
            });
            window.history.pushState({}, '', url);
        }


        elementsWithDataLoading.forEach(element => {
            let loading_classes = get_loading_class(element);
            if (loading_classes !== undefined) {
                loading_classes.forEach(loading_class => {
                    element.classList.remove(loading_class);
                });
            }
            element.style.display = "none";
        });


    }).then(el => {


    })
    elementsWithDataAttr.forEach(element => {
        let loading_attr = get_loading_attr(element);
        if (loading_attr !== undefined) {
            element.removeAttribute(loading_attr);
        }
    });
}


function onpageexpired() {
    alert("The CSRF token has expired. Please refresh the page.")
}


function update_dom(el, html) {
    let class_name = el.__liveflask['class']
    html = `<div live-component="${class_name}" id="${el.id}">${html}</div>`
    morphdom(el, html, {
        onBeforeElUpdated: function (fromEl, toEl) {
            // spec - https://dom.spec.whatwg.org/#concept-node-equals
            if (fromEl.isEqualNode(toEl)) {
                return false
            }
            return true
        },

        onElUpdated: function (element) {
            if (el.__liveflask['children'].length !== 0) {
                update_children(el.__liveflask['children'])
            }
        },

    });

    init_action(el)
}


function update_children(children = []) {
    let matched_component;
    children.forEach(i => {
        matched_component = document.getElementById(`${i.__liveflask['key']}`);
        morphdom(matched_component, i.outerHTML)
    })
}

function get_loading_class(element) {
    if (element.hasAttribute("live-loading-class")) {
        let loading_class = element.getAttribute("live-loading-class");
        if (loading_class && loading_class.includes(',')) {
            loading_class = loading_class.split(',').map(item => item.trim());
            return loading_class;
        } else {
            return [loading_class];
        }
    } else {
        return undefined;
    }
}

function get_loading_attr(element) {
    if (element.hasAttribute("live-loading-attr")) {
        let loading_attr = element.getAttribute("live-loading-attr");
        return loading_attr;
    } else {
        return undefined;
    }
}

function get_display_style(element) {
    if (element.hasAttribute("data-loading")) {
        let display_style = element.getAttribute("data-loading");
        return display_style;
    } else {
        return "block";
    }
}