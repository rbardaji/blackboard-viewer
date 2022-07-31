""" Dashboard main code."""

import socket
from dash import Dash, Output, Input
from dash.exceptions import PreventUpdate
import components as c

app = Dash(__name__, suppress_callback_exceptions=True,
           title='The Blackboard')


# Layout
app.layout = c.main_layout

@app.callback(
    Output(component_id='frames-container', component_property='children'),
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
    return [c.provider_frame(provider) for provider in providers]

for provider in c.frame_info_dict:
    @app.callback(
        Output(f'{provider}-iframe', 'children'),
        Input(f'{provider}-dropdown', 'value')
    )
    def make_provider_iframe(parameter):
        """
        Generate the provider iframe.

        Parameters
        ----------
        parameter : str
            Selected parameter.
        """
        if parameter is None:
            raise PreventUpdate
        return c.provider_iframe(provider, parameter)


if __name__ == '__main__':
    app.run_server(socket.gethostname(), 5050, debug=True)
