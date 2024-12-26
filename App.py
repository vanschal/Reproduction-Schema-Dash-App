import dash
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np

from Classes import VARIABLE, BUTTON, GRAPH, TRACE_CHECKBOXES
from Math_Utils import calculate_parameters, calculate_eigenvalues, calculate_growth_rates, calculate_r1, calculate_transformation_vectors, calculate_exponentials
from Graph_Utils import handle_balanced_growth, create_trace, CTX, T_RANGE

app = dash.Dash(__name__)
app.layout = html.Div([
    # Title and Subheading
    html.H2("Marx's Reproduction Schema", style={'textAlign': "center"}),
    # Main Layout
    html.Div([
        # Left Column: Controls
        # This portion of the layout is for the variables that can be adjusted by the user
        # Below are the elementary/basic variables
        html.Div([
            VARIABLE("Rate of Exploitation (e)", "e", 0, 10, 0.1, 1).create_component(),
            html.Br(),

            VARIABLE("Composition of Capital for Department 1 (K1)", "k1", 0, 10, 0.1, 1.5).create_component(),
            html.Br(),

            VARIABLE("Composition of Capital for Department 2 (K2)", "k2", 0, 10, 0.1, 3.2).create_component(),
            html.Br(),

            VARIABLE("Rate of Reinvestment (a)", "a", 0, 0.99, 0.1, 0.5).create_component(),
            html.Br(),

            # Initial Value Output for Department 1 and Button
            html.Div([
                VARIABLE("Initial Value Output for Department 1 (Y1i)", "y1i", 0, 10, 0.1, 1).create_component(),
                BUTTON("Balanced Growth y1i", "balanced-growth-button-y2i", "green").create_component()
            ], style={'marginBottom': '10px'}),
            html.Br(),

            # Initial Value Output for Department 2 and Button
            html.Div([
                VARIABLE("Initial Value Output for Department 2 (Y2i)", "y2i", 0, 10, 0.1, 1).create_component(),
                BUTTON("Balanced Growth y2i", "balanced-growth-button-y1i", "green").create_component()
            ], style={'marginBottom': '10px'}),
    
            BUTTON("Reset View", "reset-view-button", "red").create_component()
        ], style={'width': '30%', 'padding': '5px', 'display': 'flex', 'flexDirection': 'column'}),

    # Right Column: Graph
        html.Div([
          TRACE_CHECKBOXES(checklist_id='trace-selector').create_component(),
        GRAPH("graph").create_component(),
        ], style={'width': '80%','display':'flex'}),
    ], style = {'display': 'flex'})
])

@app.callback(
    # Outputs
    Output('graph', 'figure'),
    
    Output('slider-e', 'value'),
    Output('input-e', 'value'),
    
    Output('slider-k1', 'value'),
    Output('input-k1', 'value'),
    
    Output('slider-k2', 'value'),
    Output('input-k2', 'value'),
    
    Output('slider-a', 'value'),
    Output('input-a', 'value'),
    
    Output('slider-y1i', 'value'),
    Output('input-y1i', 'value'),
    
    Output('slider-y2i', 'value'),
    Output('input-y2i', 'value'),
    
    Output('balanced-growth-button-y1i', 'n_clicks'),
    Output('balanced-growth-button-y2i', 'n_clicks'),

    # Inputs: each slider input pair is passed in through here
    Input('slider-e', 'value'),
    Input('input-e', 'value'),
    
    Input('slider-k1', 'value'),
    Input('input-k1', 'value'),
    
    Input('slider-k2', 'value'),
    Input('input-k2', 'value'),
    
    Input('slider-a', 'value'),
    Input('input-a', 'value'),
    
    Input('slider-y1i', 'value'),
    Input('input-y1i', 'value'),
    
    Input('slider-y2i', 'value'),
    Input('input-y2i', 'value'),
    
    Input('balanced-growth-button-y1i', 'n_clicks'),
    Input('balanced-growth-button-y2i', 'n_clicks'),
    # For viewport extending and formatting
    Input('graph', 'relayoutData'),

    Input('reset-view-button', 'n_clicks'),

    Input('trace-selector', 'value')
)

def update_graph(
    slider_e_value, input_e_value,
    slider_k1_value, input_k1_value,
    slider_k2_value, input_k2_value,
    slider_a_value, input_a_value, 
    slider_y1i_value, input_y1i_value,
    slider_y2i_value, input_y2i_value,
    balanced_growth_button_y1i_n_clicks, balanced_growth_button_y2i_n_clicks,
    relayout_data, reset_view_clicks,
    selected_traces
):
    # Defining the context triggerid to detect whether the slider or the input box was triggered
    TRIGGER_ID = CTX.triggered[0]["prop_id"].split(".")[0]

    # To account for circular dependencies in linking the input box with the slider using context triggers
    e = input_e_value if TRIGGER_ID == 'input-e' else slider_e_value
    k1 = input_k1_value if TRIGGER_ID == 'input-k1' else slider_k1_value
    k2 = input_k2_value if TRIGGER_ID == 'input-k2' else slider_k2_value
    a = input_a_value if TRIGGER_ID == 'input-a' else slider_a_value
    y1i = input_y1i_value if TRIGGER_ID == 'input-y1i' else slider_y1i_value
    y2i = input_y2i_value if TRIGGER_ID == 'input-y2i' else slider_y2i_value

    # this is intended to account for the interaction when the user deletes the whole input box to allow them time to enter a new value to replace it
    if None in [e, k1, k2, a, y1i, y2i]:
        # Return no-op values to prevent overwriting
        return dash.no_update, e, e, k1, k1, k2, k2, a, a, y1i, y1i, y2i, y2i, balanced_growth_button_y1i_n_clicks, balanced_growth_button_y2i_n_clicks

    # This extends the range of view of the tracelines according to the user's zoom in or out
    # If the user zooms in the viewport is respected, if they zoom out the x_min and x_max are extended accordingly
    # Code segment below is all regarding the viewport of the graph
    global T_RANGE
    x_min, x_max = T_RANGE[0], T_RANGE[-1]
    if relayout_data and 'xaxis.range[0]' in relayout_data and 'xaxis.range[1]' in relayout_data:
        x_min = relayout_data['xaxis.range[0]']
        x_max = relayout_data['xaxis.range[1]']
    if x_min < T_RANGE[0] or x_max > T_RANGE[-1]:
        T_RANGE = np.linspace(min(x_min, T_RANGE[0]) - 5, max(x_max, T_RANGE[-1]) + 5, 1000)
    else:
        x_min, x_max = x_min, x_max
    x_range = [x_min, x_max]
    #resets the viewport for the user to the starting range
    if TRIGGER_ID == 'reset-view-button':
        x_range = [-3, 14]
    
    # Doing all the necessary math and calculations
    M_11, M_12, M_21, M_22, c_1, v_1, s_1, c_2, v_2, s_2 = calculate_parameters(e, k1, k2, a)
    mu_1, mu_2 = calculate_eigenvalues(M_11, M_12, M_21, M_22)
    m_11, m_12, m_21, m_22 = calculate_growth_rates(mu_1, mu_2, M_11, M_12)
    
    # Handles the pressing of the respective balanced growth buttons
    y1i, y2i, balanced_growth_button_y1i_n_clicks, balanced_growth_button_y2i_n_clicks = handle_balanced_growth(
    m_11, m_12, y1i, y2i, 
    balanced_growth_button_y1i_n_clicks, 
    balanced_growth_button_y2i_n_clicks
    )

    # More calculations
    r1 = calculate_r1(m_11, m_12, m_21, m_22, y1i, y2i)
    eta_vec = calculate_transformation_vectors(m_11, m_12, m_21, m_22, y1i, y2i)
    exp_1, exp_2, z_l1, z_l2 = calculate_exponentials(mu_1, mu_2, T_RANGE, k1, k2, r1, m_11, m_12)

    # Defining tracelines
    y_1 = (exp_1 * eta_vec[0] * m_11) + (exp_2 * eta_vec[1] * m_21)
    y_2 = (exp_1 * eta_vec[0] * m_12) + (exp_2 * eta_vec[1] * m_22)

    # Main traces
    trace_y1 = create_trace(T_RANGE, y_1, 'y_1', 'blue')
    trace_y2 = create_trace(T_RANGE, y_2, 'y_2', 'red')
    trace_zl1 = create_trace(T_RANGE, z_l1, 'z_l1', 'blue', dash='dash')
    trace_zl2 = create_trace(T_RANGE, z_l2, 'z_l2', 'red', dash='dash')
    # Traces for the compositions of capital
    trace_k1 = create_trace(T_RANGE, [k1] * len(T_RANGE), 'k1', 'green', dash='dot')
    trace_k2 = create_trace(T_RANGE, [k2] * len(T_RANGE), 'k2', 'purple', dash='dot')

    trace_map = {
        'y1': trace_y1,
        'y2': trace_y2,
        'zl1': trace_zl1,
        'zl2': trace_zl2,
        'k1': trace_k1,
        'k2': trace_k2
    }
    # Filter out the traces that are selected by the user
    filtered_traces = [trace_map[trace_id] for trace_id in selected_traces]

    # Regarding the backdrop
    layout = go.Layout(
    title = None,
    xaxis = dict(tickmode = 'linear', dtick = 1, range = x_range),  # Use the updated x_range
    yaxis = dict(tickmode = 'linear', dtick = 1, range = [-1, 10]),  # Keep the y-axis range fixed
    showlegend = True,
    dragmode = 'pan'
    )

    fig = go.Figure(data = filtered_traces, layout=layout)
    #this is for the y = 0 aka the x axis line 
    
    fig.update_yaxes(
    showline = False,
    linewidth = 2,
    linecolor = 'black',
    zeroline = True,       # Show the zero line
    zerolinewidth = 2,
    zerolinecolor = 'black'
    )
    # Ensuring all the values are synced up upon return so the input boxes display the same value as the sliders
    slider_e_value, input_e_value = e, e
    slider_k1_value, input_k1_value = k1, k1
    slider_k2_value, input_k2_value = k2, k2
    slider_a_value, input_a_value = a, a
    slider_y1i_value, input_y1i_value = y1i, y1i
    slider_y2i_value, input_y2i_value = y2i, y2i

    return (
        fig,  # Output for 'graph.figure'
        
        slider_e_value,  # Output for 'slider-e.value'
        input_e_value,   # Output for 'input-e.value'
        
        slider_k1_value,  # Output for 'slider-k1.value'
        input_k1_value,   # Output for 'input-k1.value'
        
        slider_k2_value,  # Output for 'slider-k2.value'
        input_k2_value,   # Output for 'input-k2.value'
        
        slider_a_value,  # Output for 'slider-a.value'
        input_a_value,   # Output for 'input-a.value'
        
        slider_y1i_value,  # Output for 'slider-y1i.value'
        input_y1i_value,   # Output for 'input-y1i.value'
        
        slider_y2i_value,  # Output for 'slider-y2i.value'
        input_y2i_value,   # Output for 'input-y2i.value'
        
        balanced_growth_button_y1i_n_clicks,  # Output for 'balanced-growth-button-y1i.n_clicks'
        balanced_growth_button_y2i_n_clicks   # Output for 'balanced-growth-button-y2i.n_clicks'
    )

if __name__ == '__main__':
    app.run_server(debug=True)