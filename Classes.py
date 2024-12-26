from dash import dcc, html

# color constants for ease of referral
COLORS = {
    'green': '#28a745',   
    'red': '#c61a09',     
    'white': '#ffffff',
    'blue': '#007bff'    
}

class VARIABLE:
    """
    A class to encapsulate a labeled slider and input component for use in a Dash application.

    This class creates a UI component consisting of a `dcc.Slider` and a `dcc.Input`, 
    linked together with a shared variable ID for consistent user input.

    Attributes:
        label (str): The label to display above the slider and input box.
        slider_id (str): The unique ID for the slider, prefixed with 'slider-'.
        input_id (str): The unique ID for the input box, prefixed with 'input-'.
        min_value (float): The minimum value for the slider and input box.
        max_value (float): The maximum value for the slider and input box.
        step (float): The step size for the slider and input box.
        value (float): The initial value for the slider and input box.

    Methods:
        create_component():
            Creates and returns a Dash `html.Div` containing a label, a slider, 
            and a linked input box for user interaction.
    """
    def __init__(self, label, variable_id, min_value, max_value, step, value):
        self.label = label
        self.slider_id = f"slider-{variable_id}"
        self.input_id = f"input-{variable_id}"
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value

    def create_component(self):
        return html.Div([
            html.Label(self.label),
            dcc.Slider(
                id=self.slider_id,
                min=self.min_value,
                max=self.max_value,
                step=self.step,
                value=self.value,
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Input(
                id=self.input_id,
                type='number',
                min=self.min_value,
                max=self.max_value,
                step=self.step,
                value=self.value,
                style={'marginLeft': '2px', 'width': '60px'}
            )
        ], style={'alignItems': 'left'})
    
class BUTTON:
  """
     A class to encapsulate a styled button component for use in a Dash application.

    Attributes:
    text (str): The text displayed on the button.
    button_id (str): The unique ID for the button, used for callback identification.
    color (str): The name of the color for the button's background, mapped through the COLORS dictionary.

    Methods:
    create_component():
    Creates and returns a Dash `html.Button` with the specified styling and functionality.
    """
  def __init__(self, text, button_id, color):
        self.text = text
        self.button_id = button_id
        self.color = color
  
  def create_component(self):
        return html.Button(
            self.text,
            id=self.button_id,
            n_clicks=0,
            style={
                'backgroundColor': COLORS[self.color],
                'color': COLORS[f'white'],
                'border': 'none',
                'padding': '10px 20px',
                'textAlign': 'center',
                'fontSize': '16px',
                'margin': '10px 0',
                'cursor': 'pointer',
                'borderRadius': '5px',
            }
        )

class TRACE_CHECKBOXES:
    """
    A class to create a checklist for controlling which traces are displayed on an existing graph.

    Attributes:
        checklist_id (str): The unique ID for the checklist.
        default_traces (list): A list of default trace values to be selected.
    """
    def __init__(self, checklist_id, default_traces = ['y1', 'y2', 'zl1', 'zl2','k1','k2']):
        self.checklist_id = checklist_id
        self.default_traces = default_traces 

    def create_component(self):
        return html.Div([
            html.Label("Display"),
            dcc.Checklist(
                id=self.checklist_id,
                options=[
                    {'label': 'y1', 'value': 'y1'},
                    {'label': 'y2', 'value': 'y2'},
                    {'label': 'z_l1', 'value': 'zl1'},
                    {'label': 'z_l2', 'value': 'zl2'},
                    {'label': 'k1', 'value': 'k1'},
                    {'label': 'k2', 'value': 'k2'}
                ],
                value=self.default_traces
            )
        ], style={'fontSize':'18px', 'marginRight':'30px', 'marginBottom':'20px'})


class GRAPH:
    """
    A class to encapsulate a styled graph component for use in a Dash application.

    Attributes:
        graph_id (str): The unique ID for the graph, used for callback identification.
        height (str): The height of the graph container (default: '80vh').
        width (str): The width of the graph container (default: '70%').

    Methods:
        create_component():
            Creates and returns a Dash dcc.Graph within a styled container.
    """
    def __init__(self, graph_id, height='80vh', width='90%'):
        self.graph_id = graph_id
        self.height = height
        self.width = width

    def create_component(self):
        return html.Div(id=f'{self.graph_id}-container', children=[
            dcc.Graph(
                id=self.graph_id,
                style={'height': self.height},
                config={
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': [
                        'zoom2d', 'autoscale', 'resetscale2d', 'pan', 'zoomin2d', 'zoomout2d'
                    ],
                }
            ),
        ], style={'width': f'{self.width}'})