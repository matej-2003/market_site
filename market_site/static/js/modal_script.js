function make_modal(id) {
    let modal = $(`div.modal#${id}`);
    let modal_content = $(`div.modal#${id} div.modal_content`);
    let open_btns = $$(`[for=${id}]`);
    console.log(open_btns);
    let close_btn = ce('span');
    close_btn.classList.add('modal_close');
    close_btn.innerHTML = '&times;';
    modal_content.insertBefore(close_btn, modal_content.childNodes[0]);

    if (open_btns != null && open_btns != []) {
        for (let open_btn of open_btns) {
            open_btn.onclick = function () {
                modal.style.display = 'block';
            }
        }
    }

    close_btn.onclick = function () {
        modal.style.display = 'none';
    }

    modal.onclick = function (event) {
        if (event.target == modal && event.target != modal_content) {
            modal.style.display = 'none';
        }
    }
}

class Modal {
    constructor(content, header, footer, onclose=null) {
        this.modal = ce('div', {
            // 'id': 'add_element_modal',
            'class': 'modal',
        });
        this.modal_content = ce('div', {
            'class': 'modal_content',
        });
        this.open_btn = ce('button');
        this.open_btn.innerText = 'Open modal';
        this.close_btn = ce('span', {
            'class': 'modal_close',
        });
        this.close_btn.innerHTML = '&times;';
        this.modal_content.append(this.close_btn);
        
        this.modal_body = ce('div', {
            'class': 'modal_body',
        });
        if (header) {
            this.modal_header = ce('div', {
                'class': 'modal_header',
            });
            this.modal_header.append(header);
            this.modal_content.append(this.modal_header);
        }
        if (content) {
            this.modal_body.append(content);
            this.modal_content.append(this.modal_body);
        }
        if (footer) {
            this.modal_footer = ce('div', {
                'class': 'modal_footer',
            });
            this.modal_footer.append(footer);
            this.modal_content.append(this.modal_footer);
        }
        this.modal.append(this.modal_content);
        this.close_btn.addEventListener('click', () => {
            this.modal.style.display = 'none';
            if (onclose) {onclose();}
        });
    
        this.modal.addEventListener('click', (event) => {
            if (event.target == this.modal && event.target != this.modal_content) {
                this.modal.style.display = 'none';
                if (onclose) {onclose();}
            }
        });
        this.open_btn.addEventListener('click', () => {
            this.start();
        });
    }
    start() {
        this.modal.style.display = 'block';
        if (onclose) {onclose();}
    }

    stop() {
        this.modal.style.display = 'none';
    }
}

function start_modal(id) {
    document.getElementById(id).style.display = 'block';
}

function stop_modal(id) {
    document.getElementById(id).style.display = 'none';
}

let modals = $$('div.modal:not([modal_type=DYNAMIC_MODAL])');
// let modals = $$('div.modal');


for (let i = 0; i < modals.length; i++) {
    make_modal(modals[i].id);
}