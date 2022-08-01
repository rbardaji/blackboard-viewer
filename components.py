import requests
from dash import html, dcc

import yaml_service
# import text

# blackboard_host = 'http://DESKTOP-VHEVVKU:5000'
blackboard_host = 'http://eoscfuture.emso.eu:5000'
# Get information from The Blackboard
response = requests.get(f'{blackboard_host}/dashboard/1')
if response.status_code == 200:
    result = response.json()
    title = result['title']
    subtitle = result['subtitle']
    logo = result['logo']
    frames = result['frames']
    frame_info_dict = {}
    for frame in frames:
        response = requests.get(f'{blackboard_host}/frame/{frame}')
        if response.status_code == 200:
            result = response.json()
            frame_info_dict[result['SD_provider_abbreviation']] = result


# Init DTOs
YDTO = yaml_service.YamlDataTransferObject()

# Components
providers_checklist = dcc.Checklist(
    id='providers-checklist',
    className='providers-checklist',
    options=[acronym for acronym in frame_info_dict],
    labelClassName='label-providers-checklist'
)

main_layout = html.Div(
    className='body',
    children=[
        dcc.Store(
            id='local-state',
            storage_type='local'
        ),
        html.Div(
            className='header-container',
            children=[
                html.Div(
                    children=[
                        html.Embed(
                            className='header-logo',
                            src=logo
                        )
                    ]
                ),
                html.Div(
                    className='title-headers',
                    children=[
                        html.H1(title, style={'margin-bottom': '0px'}),
                        html.H2(subtitle, style={'margin-top': '0.5px'})
                    ]
                )
            ]
        ),
        providers_checklist,
        html.Div(
            id='frames-container',
            className='output',
            style={'display':'inline-block'}
        ),
    ]
)


# Functions to make components
def provider_title(provider):

    return html.Img(
        className='provider-logo',
        src=frame_info_dict[provider]['SD_logo_url']
    )

def provider_dropdown(provider):

    provider_info = frame_info_dict[provider]
    parameter_list = provider_info['SD_URL']['parameters']
    name_list = []
    value_list = []
    for parameter in parameter_list:
        name_list.append(parameter['name'])
        value_list.append(parameter['value'])

    return dcc.Dropdown(
        id=f'{provider}-dropdown',
        className='provider-dropdown',
        options=[
            {'label': key, 'value': f'{provider_info["SD_URL"]["base_url"]}{value}'}
            for key, value in zip(name_list, value_list)
        ],
        placeholder=f'Select {provider}'
    )

def provider_iframe(link, height, width):

    if link.split('.')[-1] in ['png', 'jpg']:
        return html.Img(
            # ATENCION: AQUI ESTO PUEDE PETAR PORQUE YO SIEMPRE SUPONGO QUE
            # TENGO UN IFRAME, NO UNA IMAGEN
            # id=f'{provider}-iframe',
            className='provider-image',
            src=link
        )
    else:
        return html.Iframe(
            # id=f'{provider}-iframe',
            className='provider-iframe',
            style={'height': height, 'width': width},
            src=link
        )

def provider_description(provider):

    provider_content = YDTO.get_provider_content(provider)
    return html.Div(
        className='provider-description',
        children=[
            dcc.Markdown(
                className='description-text',
                children=provider_content['description']
            )
        ]
    )

def provider_license(provider):

    provider_content = YDTO.get_provider_content(provider)
    return html.Div(
        className='provider-license',
        children=[
            dcc.Markdown(
                className='license-text',
                children='License :[' + provider_content['license']['name'] + \
                     '](' + provider_content['license']['url'] + ')'
            )
        ]
    )

def provider_contact(provider):

    provider_content = YDTO.get_provider_content(provider)
    return html.Div(
        className='provider-contact',
        children=[
            dcc.Markdown(
                className='contact-text',
                children='Contact : ' + provider_content['plugin_contact']
            )
        ]
    )

def provider_frame(provider):

    height = frame_info_dict[provider]["SD_height"]
    width = frame_info_dict[provider]["SD_width"]

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

    return html.Div(
        className='provider-frame',
        style={
            'height':f'{frame_info_dict[provider]["SD_height"]}',
            'width':f'{frame_info_dict[provider]["SD_width"]}'
        },
        children=[
            provider_title(provider),
            provider_dropdown(provider),
            html.Div(
                id=f'{provider}-iframe',
                style={
                    'height':f'{height}',
                    'width':f'{width}'
                },
                children=[
                    provider_iframe(
                        frame_info_dict[provider]['SD_URL']['base_url'] + \
                        frame_info_dict[provider]['SD_URL']['parameters'][0]['value'],
                        iframe_height,
                        iframe_width
                    ),
                ]
            ),
        ]
    )

def provider_tabs(provider):

    provider_content = YDTO.get_provider_content(provider)
    return html.Div(
        className='provider-tabs',
        children=[
            dcc.Tabs(
                id=f'{provider}-tabs',
                className='provider-tabs',
                children=[
                    dcc.Tab(
                        id=f'{provider}-tab-1',
                        className='the-tab',
                        label='Description',
                        children=[
                            provider_title(provider),
                            provider_dropdown(provider),
                            # Get the first parameter
                            provider_iframe(
                                provider_content['SD_URL']['base_url'] + \
                                list(provider_content['SD_URL']['parameters'].values())[0]
                            ),
                        ]
                    ),
                    dcc.Tab(
                        id=f'{provider}-tab-2',
                        className='the-tab',
                        label='License',
                        children=[
                            provider_title(provider),
                            provider_license(provider)
                        ]
                    ),
                    dcc.Tab(
                        id=f'{provider}-tab-3',
                        className='the-tab',
                        label='Contact',
                        children=[
                            provider_title(provider),
                            provider_contact(provider)
                        ]
                    )
                ]
            )
        ]
    )
