import plotly.graph_objs as go
import dash
import numpy as np

# Global constants used in main
CTX = dash.callback_context
T_RANGE = np.linspace(-3, 14, 1000)

def calculate_balanced_growth(m_11, m_12, y_1i, y_2i):
    bg1 = (m_12 / m_11) * y_1i
    bg2 = (m_11 / m_12) * y_2i
    return bg1, bg2

def handle_balanced_growth(m_11, m_12, y1i, y2i, 
                          balanced_growth_button_y1i_n_clicks, 
                          balanced_growth_button_y2i_n_clicks):
    bg1, bg2 = calculate_balanced_growth(m_11, m_12, y1i, y2i)

    if balanced_growth_button_y2i_n_clicks > 0:
        y1i = bg2
        balanced_growth_button_y2i_n_clicks = 0

    if balanced_growth_button_y1i_n_clicks > 0:
        y2i = bg1
        balanced_growth_button_y1i_n_clicks = 0

    return y1i, y2i, balanced_growth_button_y1i_n_clicks, balanced_growth_button_y2i_n_clicks

# This is key, the interactive learning aspect of the chart can be enabled if you fill in these boxes with their respective explanations
# By default plotly supports the display of LaTeX so you can just type as if you were in overleaf (LaTex) into the quotations and it will show
HOVER_INFORMATION = {
    'y_1': ' ',
    'y_2': ' ',
    'z_l1': ' ',
    'z_l2': ' ',
    'k1': ' ',
    'k2': ' '
}

def create_trace(x, y, name, color, dash = None):
    """
    Creates a Plotly Scatter trace.

    Args:
        x (array-like): The x-axis values for the trace.
        y (array-like): The y-axis values for the trace.
        name (str): The label for the trace.
        color (str): The color of the trace line.
        dash (str, optional): The dash style for the trace line. Defaults to None.

    Returns:
        go.Scatter: A configured Scatter trace.
    """
    return go.Scatter(
        x = x,
        y = y.flatten() if hasattr(y, "flatten") else y,
        mode ='lines',
        name =  name,
        line = dict(color=color, dash=dash),
        hovertemplate = f'{HOVER_INFORMATION[name]}<extra></extra>'
    )