/// <reference types="react" />
import { ReactWidget } from '@jupyterlab/apputils';
export declare class ReactAppWidget extends ReactWidget {
    constructor(dom: string, tok: string);
    domain: string;
    token: string;
    render(): JSX.Element;
}
