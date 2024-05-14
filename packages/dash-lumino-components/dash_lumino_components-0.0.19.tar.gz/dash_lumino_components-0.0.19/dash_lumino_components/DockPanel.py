# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DockPanel(Component):
    """A DockPanel component.
A widget which provides a flexible docking area for widgets.  
{@link https://jupyterlab.github.io/lumino/widgets/classes/dockpanel.html}
@hideconstructor

@example
//Python:
import dash
import dash_lumino_components as dlc

dock = dlc.DockPanel([
    dlc.Widget(
        "Example Content",
        id="initial-widget",
        title="Hallo",
        icon="fa fa-folder-open",
        closable=True)
], id="dock-panel")

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The widgets @type {Widget[]}.

- id (string; required):
    ID of the widget @type {string}.

- addToDom (boolean; default False):
    bool if the object has to be added to the dom directly @type
    {boolean}.

- layout (boolean | number | string | dict | list; optional):
    Layout similar to DockPanel.ILayoutConfig
    (https://phosphorjs.github.io/phosphor/api/widgets/interfaces/docklayout.ilayoutconfig.html)
    Examples: * {\"main\": {\"type\": \"tab-area\", \"widgets\":
    [\"initial-widget2\", \"initial-widget\"], \"currentIndex\": 1}} *
    {\"main\": {\"type\": \"split-area\", \"orientation\":
    \"horizontal\", \"children\": [{\"type\": \"tab-area\",
    \"widgets\": [\"initial-widget2\"], \"currentIndex\": 0},
    {\"type\": \"tab-area\", \"widgets\": [\"initial-widget\"],
    \"currentIndex\": 0}], \"sizes\": [0.5, 0.5]}} * {\"main\":
    {\"type\": \"split-area\", \"orientation\": \"vertical\",
    \"children\": [{\"type\": \"tab-area\", \"widgets\":
    [\"initial-widget2\"], \"currentIndex\": 0}, {\"type\":
    \"tab-area\", \"widgets\": [\"initial-widget\"], \"currentIndex\":
    0}], \"sizes\": [0.5, 0.5]}}  Note! Use widget id in widget
    arrays!  @type {PropTypes.any}.

- mode (string; default 'multiple-document'):
    mode for the dock panel: (\"single-document\" |
    \"multiple-document\") @type {string}.

- spacing (number; default 4):
    The spacing between the items in the panel. @type {number}.

- widgetEvent (boolean | number | string | dict | list; optional):
    Widget events @type {PropTypes.any}."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_lumino_components'
    _type = 'DockPanel'
    @_explicitize_args
    def __init__(self, children=None, id=Component.REQUIRED, mode=Component.UNDEFINED, spacing=Component.UNDEFINED, addToDom=Component.UNDEFINED, widgetEvent=Component.UNDEFINED, layout=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'addToDom', 'layout', 'mode', 'spacing', 'widgetEvent']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['children', 'id', 'addToDom', 'layout', 'mode', 'spacing', 'widgetEvent']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in ['id']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(DockPanel, self).__init__(children=children, **args)
