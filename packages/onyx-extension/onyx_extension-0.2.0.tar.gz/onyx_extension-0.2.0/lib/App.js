import React from 'react';
import { ReactWidget } from '@jupyterlab/apputils';
//import App from '../../react-prototype/src/App'
function MyComponent(domain, token) {
    return React.createElement("div", null,
        React.createElement("h1", null, "Onyx Extension"),
        React.createElement("h2", null,
            "ONYX_DOMAIN: ",
            domain),
        React.createElement("h2", null,
            "ONYX_TOKEN: ",
            token));
}
export class ReactAppWidget extends ReactWidget {
    constructor(dom, tok) {
        super();
        this.domain = dom;
        this.token = tok;
    }
    render() {
        return (MyComponent(this.domain, this.token));
    }
}
//# sourceMappingURL=App.js.map