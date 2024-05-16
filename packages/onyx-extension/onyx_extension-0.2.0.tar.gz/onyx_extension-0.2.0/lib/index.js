import { ICommandPalette, MainAreaWidget, WidgetTracker } from '@jupyterlab/apputils';
import { ILauncher } from '@jupyterlab/launcher';
import { requestAPI } from './handler';
import { ReactAppWidget } from './App';
/**
 * Initialization data for the onyx_extension extension.
 */
const plugin = {
    id: 'onyx_extension:plugin',
    description: 'Onyx-extension.',
    autoStart: true,
    optional: [ILauncher],
    requires: [ICommandPalette],
    activate: (app, palette, launcher) => {
        console.log('JupyterLab extension @onyx_extension is activated!');
        const command = 'onyx_extension';
        const category = 'Onyx';
        let domain;
        let token;
        requestAPI('settings')
            .then(data => {
            console.log(data);
            domain = data['domain'];
            token = data['token'];
        })
            .catch(reason => {
            console.error(`The onyx_extension server extension appears to be missing.\n${reason}`);
        });
        // Create a single widget
        let widget;
        app.commands.addCommand(command, {
            label: 'Onyx',
            caption: 'Onyx',
            execute: () => {
                if (!widget || widget.disposed) {
                    const content = new ReactAppWidget(domain, token);
                    widget = new MainAreaWidget({ content });
                    widget.title.label = 'Onyx';
                    widget.title.closable = true;
                }
                if (!tracker.has(widget)) {
                    tracker.add(widget);
                }
                if (!widget.isAttached) {
                    // Attach the widget to the main work area if it's not there
                    app.shell.add(widget, 'main');
                }
                // Activate the widget
                app.shell.activateById(widget.id);
            },
        });
        palette.addItem({ command, category: category });
        if (launcher) {
            // Add launcher
            launcher.add({
                command: command,
                category: category
            });
        }
    }
};
const tracker = new WidgetTracker({
    namespace: 'onyx_extension',
});
export default plugin;
//# sourceMappingURL=index.js.map