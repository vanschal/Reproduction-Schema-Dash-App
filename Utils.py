import numpy as np
import plotly.graph_objects as go

COLORS = {
    "green": "#28a745",
    "red": "#c61a09",
    "blue": "#007bff",
    "white": "#ffffff"
}

def generate_heatmap(bs_model, current_price, strike, volatility):
    spot_range = np.linspace(current_price * 0.8, current_price * 1.2, 10)
    vol_range = np.linspace(volatility * 0.5, volatility * 1.5, 10)

    call_prices = np.zeros((len(vol_range), len(spot_range)))
    put_prices = np.zeros((len(vol_range), len(spot_range)))

    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            bs_temp = BlackScholes(bs_model.time_to_maturity, strike, spot, vol, bs_model.interest_rate)
            call, put = bs_temp.calculate_prices()
            call_prices[i, j] = call
            put_prices[i, j] = put

    fig_call = go.Figure(data=go.Heatmap(z=call_prices, x=spot_range, y=vol_range, colorscale="Viridis"))
    fig_call.update_layout(title="Call Option Prices", xaxis_title="Spot Price", yaxis_title="Volatility")

    fig_put = go.Figure(data=go.Heatmap(z=put_prices, x=spot_range, y=vol_range, colorscale="Viridis"))
    fig_put.update_layout(title="Put Option Prices", xaxis_title="Spot Price", yaxis_title="Volatility")

    return fig_call, fig_put
