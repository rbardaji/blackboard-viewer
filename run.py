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
        # Search for the provider, THIS MUST BE CHANGED
        provider_call = ''
        for provider_search in c.frame_info_dict:
            if c.frame_info_dict[provider_search]["SD_URL"]["base_url"] in parameter:
                provider_call = provider_search
                break
        height = c.frame_info_dict[provider_call]['SD_height']
        width = c.frame_info_dict[provider_call]['SD_width']
        if 'px' in height:
            height_number = int(height.split('px')[0])
            width_number = int(width.split('px')[0])

            iframe_height = f'{height_number - 2}px'
            iframe_width = f'{width_number - 2}px'

        elif 'rem' in height:
            height_number = float(height.split('rem')[0])
            width_number = float(width.split('rem')[0])

            iframe_height = f'{height_number - 10.7}rem'
            iframe_width = f'{width_number - 1.5}rem'

        elif 'rm' in height:
            height_number = float(height.split('rm')[0])
            width_number = float(width.split('rm')[0])

            iframe_height = f'{height_number - 2}rm'
            iframe_width = f'{width_number - 2}rm'

        return c.provider_iframe(parameter, iframe_height, iframe_width)


if __name__ == '__main__':
    app.run_server(socket.gethostname(), 5050, debug=True)
