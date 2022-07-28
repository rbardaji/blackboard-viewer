""" Dashboard main code."""

import socket
from dash import Dash, Output, Input
from dash.exceptions import PreventUpdate
import components as c

app = Dash(__name__, suppress_callback_exceptions=True,
           title='ENVRI - State of the Environment')


# Layout
app.layout = c.main_layout

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(c.providers_checklist, component_property='value')
)
def make_output_div(providers):
    """
    Generate the output div.

    Parameters
    ----------
    providers : list
        List of selected providers.
    """
    if providers is None:
        raise PreventUpdate
    return [c.provider_tabs(provider) for provider in providers]

if __name__ == '__main__':
    app.run_server(socket.gethostname(), 5050, debug=True)
