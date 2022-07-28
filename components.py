from dash import html, dcc

import yaml_service
import text

# Init DTOs
YDTO = yaml_service.YamlDataTransferObject()

# Components
providers_checklist = dcc.Checklist(
    id='providers-checklist',
    className='providers-checklist',
    options=YDTO.get_providers(),
    # inputClassName='input-providers-checklist',
    labelClassName='label-providers-checklist'
)

main_layout = html.Div(
    children=[
        dcc.Store(
            id='local-state',
            storage_type='local'
        ),
        html.Div(
            className='header-container',
            children=[
                html.Div(
                    # className='flex-child-image',
                    children=[
                        html.Img(
                            # className='header-image',
                            src='/assets/eosc-future.svg'
                        )
                    ]
                ),
                html.Div(
                    className='flex-child-headings',
                    children=[
                        html.H1(text.title),
                        html.H2(text.subtitle)
                    ]
                )
            ]
        ),
        providers_checklist,
        html.Div(
            id='my-output',
            className='output'
        ),
    ]
)


# Functions to make components
def provider_title(provider):

    provider_content = YDTO.get_provider_content(provider)
    return html.A(
        className='provider-title',
        target='_blank',
        children=[
            html.Div(
                className='tab-row-top',
                children=[
                    dcc.Markdown(
                        className='title-text',
                        children='**' + provider_content['SD_provider'] + '**'
                    ),
                    html.Img(
                        className='provider-image',
                        src=provider_content['SD_logo_url']
                    )
                ]
            )
        ]
    )

def provider_dropdown(provider):

    provider_content = YDTO.get_provider_content(provider)
    return dcc.Dropdown(
        id=f'{provider}-dropdown',
        className='provider-dropdown',
        options=[
            {'label': key, 'value': f'{provider_content["SD_URL"]}{value}'}
            for key, value in provider_content['SD_URL']['parameters'].items()
        ],
        placeholder=f'Select {provider}'
    )

def provider_iframe(link):

    if link.split('.')[-1] in ['png', 'jpg']:
        return html.Img(
            className='provider-image',
            src=link
        )
    else:
        return html.Iframe(
            className='provider-iframe',
            src=link,
            sandbox='allow-same-origin'
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
