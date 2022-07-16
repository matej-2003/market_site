// function $(e) {
//     return document.querySelector(e);
// }

function $$(e) {
    return document.querySelectorAll(e);
}

function ce(tag, properties) {
    if (properties && typeof (properties) == "object") {
        let tmp = document.createElement(tag);
        for (let key in properties) {
            switch (key) {
                case "class":
                    tmp.classList.value = properties[key];
                    // let classes = properties[key].split(' ');
                    // for (let c of classes) {
                    //     tmp.classList.add(c);
                    // }
                    break;
                default:
                    tmp.setAttribute(key, properties[key]);
                    break;
            }
        }
        return tmp;
    } else {
        return document.createElement(tag);
    }
}