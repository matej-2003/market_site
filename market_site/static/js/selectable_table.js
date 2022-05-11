
class Row {
    constructor(html, checkbox) {
        this.html = html;
        this.checkbox = checkbox;
        this.on_click = null;
        this.data = null;

        if (this.checkbox) {
            if (this.checkbox.checked) this.html.classList.toggle('selected');
            this.checkbox.addEventListener('click', () => {
                this.toggle_checkbox();
                if (this.checkbox.checked) this.html.classList.add('selected');
                else this.html.classList.remove('selected');
                if (this.on_click) this.on_click();
            });
        }
        this.html.addEventListener('click', () => {
            if (this.checkbox) {
                this.toggle_checkbox();
                if (this.on_click) this.on_click();
            }
            this.html.classList.toggle('selected');
        });
    }

    toggle_checkbox() {
        this.checkbox.checked = !this.checkbox.checked;
    }

    toggle() {
        this.checkbox.checked = !this.checkbox.checked;
        this.html.classList.toggle('selected');
    }

    clear() {
        this.checkbox.checked = false;
        this.html.classList.remove('selected');
    }

    set(condition) {
        if (this.checkbox) this.checkbox.checked = condition;
        if (condition) this.html.classList.add('selected');
        else this.html.classList.remove('selected');
    }
}

class SelectableTable {
    constructor(data = [], toolbar = false, make_row = null, on_click = null, on_all = null, on_toggle = null, on_clear = null) {
        this.table = ce('table', { 'class': 'selectable' });
        this.rows = [];

        this.all = ce('input', { 'type': 'checkbox' });
        this.all_link = ce('a', { 'href': '#' });
        this.all_link.innerText = 'all';
        this.toggle = ce('input', { 'type': 'checkbox' });
        this.toggle_link = ce('a', { 'href': '#' });
        this.toggle_link.innerText = 'toggle';
        this.clear_link = ce('a', { 'href': '#' });
        this.clear_link.innerText = 'clear';
        this.toolbar = ce('div');
        this.toolbar.append(
            this.all, this.all_link,
            ' | ',
            this.toggle, this.toggle_link,
            ' | ',
            this.clear_link,
        );

        this.on_all = on_all;
        this.on_toggle = on_toggle;
        this.on_clear = on_clear;

        this.all.addEventListener('click', () => {
            this.all_(this.all.checked);
        });

        this.all_link.addEventListener('click', () => {
            this.all.checked = !this.all.checked;
            this.all_(this.all.checked);
        });

        this.toggle.addEventListener('click', () => {
            this.toggle_();
        });

        this.toggle_link.addEventListener('click', () => {
            this.toggle.checked = !this.toggle.checked;
            this.toggle_();
        });

        this.clear_link.addEventListener('click', () => {
            this.clear_();
        });

        if (toolbar) {
            toolbar.append(this.toolbar);
        } else {
            let tr = this.table.insertRow(0);
            tr.classList.add('toolbar');
            let td = tr.insertCell(0);
            td.setAttribute("colspan", "100");
            td.appendChild(this.toolbar);
        }

        for (let datum of data) {
            let row = make_row(datum, on_click);
            row.data = datum;
            row.on_click = on_click;
            this.rows.push(row);
            this.table.appendChild(row.html);
        }
    }

    get_selected() {
        let selected = [];
        for (let row of this.rows) {
            if (row.checkbox.checked) selected.push(row.data);
        }
        return selected;
    }

    all_(condition) {
        this.toggle.checked = false;
        for (let row of this.rows) {
            row.set(condition);
        }
        if (this.on_all) this.on_all();
    }

    toggle_() {
        this.all.checked = false;
        for (let row of this.rows) {
            row.toggle();
        }
        if (this.on_toggle) this.on_toggle();
    }

    clear_() {
        this.all.checked = false;
        this.toggle.checked = false;
        for (let row of this.rows) {
            row.clear();
        }
        if (this.on_clear) this.on_clear();
    }
}

function load_s_table(s_table) {
    let rows = s_table.querySelectorAll('tr:not(.toolbar)');
    let all = ce('input', { 'type': 'checkbox' });
    let all_link = ce('a', { 'href': '#' });
    all_link.innerText = 'all';
    let toggle = ce('input', { 'type': 'checkbox' });
    let toggle_link = ce('a', { 'href': '#' });
    toggle_link.innerText = 'toggle';
    let clear_link = ce('a', { 'href': '#' });
    clear_link.innerText = 'clear';

    all.addEventListener('click', () => {
        all_(all.checked);
    });

    all_link.addEventListener('click', () => {
        all.checked = !all.checked;
        all_(all.checked);
    });

    toggle.addEventListener('click', () => {
        toggle_();
    });

    toggle_link.addEventListener('click', () => {
        toggle.checked = !toggle.checked;
        toggle_();
    });

    clear_link.addEventListener('click', () => {
        clear_();
    });

    function all_(condition) {
        for (let row of rows) {
            let chk = row.querySelector('input[type=checkbox]');
            if (chk) chk.checked = condition;
            if (condition) row.classList.add('selected');
            else row.classList.remove('selected');
        }
        toggle.checked = false;
    }

    function toggle_() {
        for (let row of rows) {
            let chk = row.querySelector('input[type=checkbox]');
            if (chk) chk.checked = !chk.checked;
            row.classList.toggle('selected');
        }
        all.checked = false;
    }

    function clear_() {
        all.checked = false;
        toggle.checked = false;
        for (let row of rows) {
            let chk = row.querySelector('input[type=checkbox]');
            if (chk) chk.checked = false;
            row.classList.remove('selected');
        }
    }

    if (s_table.classList.contains('toolbar')) {
        let tr = s_table.insertRow(0);
        tr.classList.add('toolbar');
        let td = tr.insertCell(0);
        td.setAttribute("colspan", "100");

        td.append(
            all, all_link,
            ' | ',
            toggle, toggle_link,
            ' | ',
            clear_link,
        );
    } else {
        let toolbar = $(`.toolbar[for=${s_table.id}]`);
        if (toolbar) {
            toolbar.append(
                all, all_link,
                ' | ',
                toggle, toggle_link,
                ' | ',
                clear_link,
            );
        }
    }

    for (let row of rows) {
        let chk = row.querySelector('input[type=checkbox]');
        if (chk) {
            if (chk.checked) row.classList.toggle('selected');
            chk.addEventListener('click', () => {
                chk.checked = !chk.checked;
                if (chk.checked) row.classList.add('selected');
                else row.classList.remove('selected');
            });
        }
        row.addEventListener('click', () => {
            if (chk) {
                chk.checked = !chk.checked;
            }
            row.classList.toggle('selected');
        });

    }
}
let s_tables = $$('table.selectable');

for (let st of s_tables) {
    load_s_table(st);
}
