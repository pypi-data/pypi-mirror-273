///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// INITIALIZERS
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

window.liveflask = {
    components: [],
    first: function () {
        return this.components.length > 0 ? this.components[0] : null;
    },
    find: function (id) {
        return this.components.find(component => component.data.key === id) || null;
    },
    get_by_name: function (name) {
        return this.components.filter(component => component.class === name);
    },
    all: function () {
        return this.components;
    },
}

document.querySelectorAll('[live-component]').forEach(el => {
    let live_flask_children = [];
    let elementsWithDataLoading = el.querySelectorAll('[live-loading]');
    let elements_with_offline_directive = el.querySelectorAll('[live-offline]');


    el.__liveflask = JSON.parse(el.getAttribute('live-snapshot'));
    el.removeAttribute('live-snapshot')


    elementsWithDataLoading.forEach(element => {
        element.style.display = "none";
    });

    elements_with_offline_directive.forEach(element => {
        element.style.display = "none";
    });


    init_model(el)
    init_action(el)
    init_polling(el)


    el.__liveflask.set = function (key, value) {
        el.__liveflask[key] = value
        send_request(el, {update_property: [key, value]}, undefined)
    }

    window.liveflask.components.push(el.__liveflask);

    // register event named liveflask:initialized
    document.dispatchEvent(new CustomEvent('liveflask:initialized', {detail: el.__liveflask, target: el}))
    init_inits(el)

})


window.addEventListener('online', function (event) {
    let elements_with_offline_directive = document.querySelectorAll('[live-offline]');
    elements_with_offline_directive.forEach(element => {
        element.style.display = "none";
    });
});

window.addEventListener('offline', function (event) {
    let elements_with_offline_directive = document.querySelectorAll('[live-offline]');
    elements_with_offline_directive.forEach(element => {
        element.style.display = "block";
    });
});