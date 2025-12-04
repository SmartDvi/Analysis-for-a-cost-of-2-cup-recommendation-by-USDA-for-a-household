import dash_mantine_components as dmc
import dash
import dash_ag_grid as dag
from dash import dcc, html, Input, Output, State, callback, Dash
import pandas as pd
from utils import *
from dash_iconify import DashIconify

app = Dash(__name__, external_stylesheets=dmc.styles.ALL)

# Theme toggle component
theme_toggle = dmc.ActionIcon(
    [
        dmc.Paper(DashIconify(icon="radix-icons:sun", width=20), darkHidden=True),
        dmc.Paper(DashIconify(icon="radix-icons:moon", width=20), lightHidden=True),
    ],
    variant="filled",
    color="yellow",
    id="color-scheme-toggle",
    size="lg",
    style={'position': 'absolute', 'right': 20, 'top': 20}
)

# Professional header
head = dmc.Paper(
    p='xl',
    mb='xl',
    style={
        'background': colors['accent_gradient'],
        'borderRadius': '12px',
        'position': 'relative',
        'boxShadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
    },
    children=[
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Stack(
                            [
                                dmc.Title(
                                    "🍎 Fruit & Vegetable Affordability Dashboard",
                                    order=1,
                                    c='white',
                                    size='h2',
                                    fw=800,
                                ),
                                dmc.Text(
                                    "Analyzing nutritional costs across household types and budget levels",
                                    c='white',
                                    size='lg',
                                    opacity=0.9
                                ),
                            ],
                            gap=0
                        ),
                        theme_toggle,
                    ],
                    justify='space-between'
                ),
                dmc.Group(
                    [
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:fruit-cherries", width=24, color=colors['success']),
                                    dmc.Stack([
                                        dmc.Text("Total Items", size='xs', c='white', opacity=0.8),
                                        dmc.Title(str(summary_stats['total_items']), order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:currency-usd", width=24, color=colors['warning']),
                                    dmc.Stack([
                                        dmc.Text("Avg Price/Cup", size='xs', c='white', opacity=0.8),
                                        dmc.Title(f"${summary_stats['avg_price']:.2f}", order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:home-group", width=24, color=colors['secondary']),
                                    dmc.Stack([
                                        dmc.Text("Household Types", size='xs', c='white', opacity=0.8),
                                        dmc.Title(str(len(household_types)), order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:chart-box", width=24, color=colors['primary']),
                                    dmc.Stack([
                                        dmc.Text("Price Range", size='xs', c='white', opacity=0.8),
                                        dmc.Title(summary_stats['price_range'], order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                    ],
                    grow=True,
                    gap='md'
                )
            ],
            gap='lg'
        )
    ]
)

# Filters section
filter_section = dmc.Paper(
    p='md',
    mb='xl',
    style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["card_border"]}',
        'borderRadius': '8px',
        'boxShadow': '0 1px 3px 0 rgba(0, 0, 0, 0.05)'
    },
    children=[
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Title("Data Filters", order=4, c=colors['text_primary']),
                        DashIconify(icon="mdi:filter-variant", width=20, color=colors['primary'])
                    ],
                    gap='sm'
                ),
                dmc.Group(
                    [
                        dmc.MultiSelect(
                            id='fruit-dropdown',
                            label='Select Fruits',
                            placeholder='Choose fruits...',
                            data=[{'value': fruit, 'label': fruit} for fruit in sorted(df['Fruit'].unique())],
                            value=[],
                            style={'width': 250},
                            clearable=True,
                            searchable=True,
                            #icon=DashIconify(icon="fluent:food-apple-24-regular")
                        ),
                        dmc.Select(
                            id='CupEquivalentUnit-dropdown',
                            label='Cup Equivalent Unit',
                            placeholder='All units',
                            data=[{'value': unit, 'label': unit} for unit in sorted(df['CupEquivalentUnit'].unique())],
                            value=None,
                            style={'width': 200},
                            clearable=True,
                            #icon=DashIconify(icon="mdi:cup")
                        ),
                        dmc.Select(
                            id='price-category-dropdown',
                            label='Price Category',
                            placeholder='All categories',
                            data=[{'value': cat, 'label': cat} for cat in sorted(df['CupEquivalentPriceCategory'].cat.categories)],
                            value=None,
                            style={'width': 200},
                            clearable=True,
                            #icon=DashIconify(icon="mdi:tag")
                        ),
                        dmc.Button(
                            "Clear Filters",
                            id='clear-filters',
                            variant='light',
                            color='gray',
                            leftSection=DashIconify(icon="mdi:filter-remove")
                        )
                    ],
                    gap='md'
                )
            ],
            gap='md'
        )
    ]
)

# Custom calculator section
custom_calculator = dmc.Paper(
    p='md',
    style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["card_border"]}',
        'borderRadius': '8px',
        'height': '100%'
    },
    children=[
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Title("Custom Calculator", order=4, c=colors['text_primary']),
                        DashIconify(icon="mdi:calculator", width=24, color=colors['primary'])
                    ],
                    justify='space-between'
                ),
                dmc.Text(
                    "Configure your household for personalized cost estimates",
                    size='sm', c=colors['text_secondary']
                ),
                dmc.Divider(),

                # Household configuration
                dmc.Stack(
                    [
                        dmc.NumberInput(
                            id='adults-input',
                            label='Adults',
                            min=0,
                            max=10,
                            value=2,
                            description='Age 19+',
                            leftSection=DashIconify(icon="mdi:account"),
                            style={'width': '100%'}
                        ),
                        dmc.NumberInput(
                            id='children-input',
                            label='Children',
                            min=0,
                            max=10,
                            value=2,
                            description='Ages 2-13',
                            leftSection=DashIconify(icon="mdi:account-child"),
                            style={'width': '100%'}
                        ),
                        dmc.NumberInput(
                            id='teens-input',
                            label='Teens',
                            min=0,
                            max=10,
                            value=0,
                            description='Ages 14-18',
                            leftSection=DashIconify(icon="mdi:account-supervisor"),
                            style={'width': '100%'}
                        ),
                    ],
                    gap='sm'
                ),

                # Consumption preferences
                dmc.Stack(
                    [
                        dmc.Select(
                            id='consumption-form',
                            label='Preferred Form',
                            value='Fresh',
                            data=[{'value': form, 'label': form} for form in df['Form'].unique()],
                            leftSection=DashIconify(icon="mdi:food-apple"),
                            style={'width': '100%'}
                        ),
                        dmc.MultiSelect(
                            id='picked-fruits',
                            label='Preferred Fruits',
                            placeholder='Select fruits...',
                            data=[{'value': fruit, 'label': fruit} for fruit in sorted(df['Fruit'].unique())],
                            value=['Apples', 'Bananas', 'Oranges'],
                            searchable=True,
                            style={'width': '100%'}
                        ),
                    ],
                    gap='sm'
                ),

                dmc.Button(
                    "Calculate Estimate",
                    id='get-cost-estimate-btn',
                    variant='gradient',
                    gradient={'from': colors['primary'], 'to': colors['secondary']},
                    fullWidth=True,
                    leftSection=DashIconify(icon="mdi:calculator")
                ),

                # Results section
                dmc.Divider(label="Results"),
                html.Div(id='cost-estimate-results')
            ],
            gap='md'
        )
    ]
)

# Define column definitions for AG Grid
column_defs = []
for col in household_costs_df.columns:
    col_def = {
        'headerName': col.replace('_', ' ').title(),
        'field': col,
        'sortable': True,
        'filter': True,
        'resizable': True,
    }

    if any(x in col.lower() for x in ['cost', 'price']):
        col_def['type'] = 'numericColumn'
        col_def['valueFormatter'] = {'function': 'd3.format("$,.2f")(params.value)'}
    elif any(x in col.lower() for x in ['cups', 'members', 'adults', 'children', 'teens']):
        col_def['type'] = 'numericColumn'
        col_def['valueFormatter'] = {'function': 'd3.format(".1f")(params.value)'}

    column_defs.append(col_def)

# Price categories tabs - Enhanced version
price_categories_tabs = dmc.Paper(
    p=0,
    mb='xl',
    style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["card_border"]}',
        'borderRadius': '8px'
    },
    children=dmc.Tabs(
        [
            dmc.TabsList(
                [
                    dmc.Tabs(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd-off", width=18),
                            dmc.Text("Low Budget", size='sm')
                        ], gap='xs'),
                        value='low-budget'
                    ),
                    dmc.Tabs(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd", width=18),
                            dmc.Text("Budget", size='sm')
                        ], gap='xs'),
                        value='budget'
                    ),
                    dmc.Tabs(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd-circle", width=18),
                            dmc.Text("Moderate", size='sm')
                        ], gap='xs'),
                        value='moderate'
                    ),
                    dmc.Tabs(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd-circle-outline", width=18),
                            dmc.Text("High Budget", size='sm')
                        ], gap='xs'),
                        value='high-budget'
                    ),
                ],
                grow=True
            ),

            # Low Budget Tab
            dmc.TabsPanel(
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Low Budget Analysis", order=3, c=colors['text_primary']),
                        dmc.Badge("Most Affordable", color="green", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced in the lowest 25% quartile - ideal for cost-conscious households",
                        size='sm', c=colors['text_secondary']
                    ),
                    dmc.Divider(),
                    dmc.Grid([
                        dmc.GridCol(span=6, children=[
                            dcc.Graph(
                                id='low-budget-chart',
                                figure=create_category_analysis('Low Budget'),
                                style={'height': 400}
                            )
                        ]),
                        dmc.GridCol(span=6, children=[
                            dmc.Paper(
                                p='md',
                                style={'background': colors['background'], 'borderRadius': '8px'},
                                children=[
                                    dmc.Title("Key Insights", order=5, mb='md'),
                                    dmc.Stack([
                                        dmc.Group([
                                            DashIconify(icon="mdi:check-circle", color=colors['success']),
                                            dmc.Text("Average Price: ", size='sm', fw=500),
                                            dmc.Text(f"${price_benchmarks['low']:.2f}/cup", size='sm')
                                        ], gap='xs'),
                                        dmc.Group([
                                            DashIconify(icon="mdi:check-circle", color=colors['success']),
                                            dmc.Text("Items Count: ", size='sm', fw=500),
                                            dmc.Text(str(summary_stats['budget_items']), size='sm')
                                        ], gap='xs'),
                                        dmc.Group([
                                            DashIconify(icon="mdi:check-circle", color=colors['success']),
                                            dmc.Text("Savings Potential: ", size='sm', fw=500),
                                            dmc.Text(f"{(1 - price_benchmarks['low']/price_benchmarks['avg'])*100:.0f}% vs average", size='sm')
                                        ], gap='xs'),
                                    ], gap='sm')
                                ]
                            )
                        ])
                    ], gutter='md')
                ], gap='md'),
                value='low-budget'
            ),

            # Budget Tab
            dmc.TabsPanel(
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Budget Analysis", order=3, c=colors['text_primary']),
                        dmc.Badge("Value for Money", color="blue", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced between 25% and 50% quartile - balanced quality and affordability",
                        size='sm', c=colors['text_secondary']
                    ),
                    dmc.Divider(),
                    dcc.Graph(
                        id='budget-chart',
                        figure=create_category_analysis('Budget'),
                        style={'height': 400}
                    )
                ], gap='md'),
                value='budget'
            ),

            # Moderate Tab
            dmc.TabsPanel(
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Moderate Analysis", order=3, c=colors['text_primary']),
                        dmc.Badge("Premium Quality", color="orange", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced between 50% and 75% quartile - higher quality options",
                        size='sm', c=colors['text_secondary']
                    ),
                    dmc.Divider(),
                    dcc.Graph(
                        id='moderate-chart',
                        figure=create_category_analysis('Moderate'),
                        style={'height': 400}
                    )
                ], gap='md'),
                value='moderate'
            ),

            # High Budget Tab
            dmc.TabsPanel(
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("High Budget Analysis", order=3, c=colors['text_primary']),
                        dmc.Badge("Premium Selection", color="red", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced in the highest 25% quartile - premium and specialty items",
                        size='sm', c=colors['text_secondary']
                    ),
                    dmc.Divider(),
                    dcc.Graph(
                        id='high-budget-chart',
                        figure=create_category_analysis('High Budget'),
                        style={'height': 400}
                    )
                ], gap='md'),
                value='high-budget'
            ),
        ],
        value='low-budget',
        orientation='horizontal'
    )
)

# Main app layout
app.layout = dmc.MantineProvider(
    theme={
        'colorScheme': 'light',
        'primaryColor': 'blue',
        'fontFamily': 'Inter, -apple-system, BlinkMacSystemFont, sans-serif',
        'headings': {'fontFamily': 'Inter, sans-serif', 'fontWeight': 600}
    },
    children=[
        dmc.Container(
            fluid=True,
            size='xl',
            p='md',
            children=[
                head,
                
                filter_section,

                # Main content grid
                dmc.Grid(
                    [
                        # Left column - Visualizations
                        dmc.GridCol(
                            span=8,
                            children=dmc.Stack(
                                [
                                    # Price distribution
                                    dmc.Paper(
                                        p='md',
                                        style={
                                            'background': colors['card_bg'],
                                            'border': f'1px solid {colors["card_border"]}',
                                            'borderRadius': '8px'
                                        },
                                        children=[
                                            dmc.Title("Price Distribution Analysis", order=3, mb='md'),
                                            dcc.Graph(
                                                id='price-distribution-chart',
                                                figure=create_price_distribution(),
                                                style={'height': 450}
                                            )
                                        ]
                                    ),

                                    # Price categories tabs
                                    price_categories_tabs,

                                    # Household cost comparison
                                    dmc.Paper(
                                        p='md',
                                        style={
                                            'background': colors['card_bg'],
                                            'border': f'1px solid {colors["card_border"]}',
                                            'borderRadius': '8px'
                                        },
                                        children=[
                                            dmc.Stack([
                                                dmc.Group([
                                                    dmc.Title("Household Cost Comparison", order=3),
                                                    dmc.Select(
                                                        id='period-selector',
                                                        value='Weekly',
                                                        data=['Daily', 'Weekly', 'Monthly', 'Yearly'],
                                                        style={'width': 150}
                                                    )
                                                ], justify='space-between'),
                                                dcc.Graph(
                                                    id='household-cost-chart',
                                                    figure=create_household_cost_comparison('Weekly'),
                                                    style={'height': 400}
                                                )
                                            ], gap='md')
                                        ]
                                    )
                                ],
                                gap='xl'
                            )
                        ),

                        # Right column - Calculator and Data
                        dmc.GridCol(
                            span=4,
                            children=dmc.Stack(
                                [
                                    custom_calculator,

                                    # Affordability matrix
                                    dmc.Paper(
                                        p='md',
                                        style={
                                            'background': colors['card_bg'],
                                            'border': f'1px solid {colors["card_border"]}',
                                            'borderRadius': '8px'
                                        },
                                        children=[
                                            dmc.Title("Affordability Matrix", order=3, mb='md'),
                                            dcc.Graph(
                                                id='affordability-matrix',
                                                figure=create_affordability_matrix(),
                                                style={'height': 350}
                                            )
                                        ]
                                    ),

                                    # Data table
                                    dmc.Paper(
                                        p='md',
                                        style={
                                            'background': colors['card_bg'],
                                            'border': f'1px solid {colors["card_border"]}',
                                            'borderRadius': '8px'
                                        },
                                        children=[
                                            dmc.Stack([
                                                dmc.Group([
                                                    dmc.Title("Household Cost Data", order=3),
                                                    dmc.Badge(
                                                        f"{len(household_costs_df)} Households",
                                                        color="blue"
                                                    )
                                                ], justify='space-between'),
                                                dag.AgGrid(
                                                    id='household-data-table',
                                                    columnDefs=column_defs,
                                                    rowData=household_costs_df.reset_index().to_dict('records'),
                                                    defaultColDef={
                                                        'resizable': True,
                                                        'sortable': True,
                                                        'filter': True,
                                                        'flex': 1,
                                                        'minWidth': 150
                                                    },
                                                    dashGridOptions={
                                                        'pagination': True,
                                                        'paginationPageSize': 10,
                                                        'domLayout': 'autoHeight',
                                                        'animateRows': True,
                                                        'rowSelection': 'single'
                                                    },
                                                    style={'width': '100%', 'height': 400}
                                                )
                                            ], gap='md')
                                        ]
                                    )
                                ],
                                gap='xl'
                            )
                        )
                    ],
                    gutter='xl'
                ),

                # Footer
                dmc.Center(
                    dmc.Text(
                        [
                            "Dashboard developed with ",
                            dmc.Text("Plotly Dash", c=colors['primary'], fw=600),
                            " • Data Source: Fruit and Vegetables Price Dataset • ",
                            dmc.Text("USDA Recommendations", c=colors['secondary'], fw=600)
                        ],
                        size='sm',
                        c=colors['text_secondary'],
                        mt='xl',
                        mb='md'
                    )
                )
            ]
        )
    ]
)

# Callbacks
@callback(
    Output('price-distribution-chart', 'figure'),
    Output('household-cost-chart', 'figure'),
    Input('fruit-dropdown', 'value'),
    Input('CupEquivalentUnit-dropdown', 'value'),
    Input('price-category-dropdown', 'value'),
    Input('period-selector', 'value')
)
def update_charts(fruits, unit, price_category, period):
    # Filter data
    filtered_df = df.copy()

    if fruits:
        filtered_df = filtered_df[filtered_df['Fruit'].isin(fruits)]
    if unit:
        filtered_df = filtered_df[filtered_df['CupEquivalentUnit'] == unit]
    if price_category:
        filtered_df = filtered_df[filtered_df['CupEquivalentPriceCategory'] == price_category]

    # Update price distribution
    fig1 = create_price_distribution()
    if len(filtered_df) > 0:
        # Update histogram with filtered data
        fig1.data[0].x = filtered_df['CupEquivalentPrice']

    # Update household cost comparison
    fig2 = create_household_cost_comparison(period)

    return fig1, fig2

@callback(
    Output('cost-estimate-results', 'children'),
    Input('get-cost-estimate-btn', 'n_clicks'),
    State('adults-input', 'value'),
    State('children-input', 'value'),
    State('teens-input', 'value'),
    State('consumption-form', 'value'),
    State('picked-fruits', 'value')
)
def calculate_cost_estimate(n_clicks, adults, children, teens, form, fruits):
    if n_clicks is None:
        return dmc.Alert(
            "Configure your household and click 'Calculate Estimate' to see results",
            color="blue",
            variant="light"
        )

    # Calculate daily cups
    household_config = {'adults': adults, 'children': children, 'teens': teens}
    cups_data = calculate_daily_cups(household_config)

    # Filter prices based on selected fruits and form
    if fruits:
        fruit_prices = df[df['Fruit'].isin(fruits)]
        if form:
            fruit_prices = fruit_prices[fruit_prices['Form'] == form]
        avg_price = fruit_prices['CupEquivalentPrice'].mean()
    else:
        avg_price = price_benchmarks['avg']

    # Calculate costs
    daily_cost = cups_data['total'] * avg_price
    weekly_cost = daily_cost * 7
    monthly_cost = daily_cost * 30
    yearly_cost = daily_cost * 365

    return dmc.Stack([
        dmc.Group([
            dmc.Paper([
                dmc.Text("Daily Cost", size='xs', c=colors['text_secondary']),
                dmc.Title(f"${daily_cost:.2f}", order=4, c=colors['text_primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
            dmc.Paper([
                dmc.Text("Weekly Cost", size='xs', c=colors['text_secondary']),
                dmc.Title(f"${weekly_cost:.2f}", order=4, c=colors['text_primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
        ], grow=True),
        dmc.Group([
            dmc.Paper([
                dmc.Text("Monthly Cost", size='xs', c=colors['text_secondary']),
                dmc.Title(f"${monthly_cost:.2f}", order=4, c=colors['text_primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
            dmc.Paper([
                dmc.Text("Yearly Cost", size='xs', c=colors['text_secondary']),
                dmc.Title(f"${yearly_cost:.2f}", order=4, c=colors['text_primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
        ], grow=True),
        dmc.Alert(
            f"Estimated annual cost for {adults} adult(s), {children} child(ren), and {teens} teen(s): ${yearly_cost:,.0f}",
            title="Cost Summary",
            color="green",
            variant="light"
        )
    ], gap='sm')

@callback(
    Output('fruit-dropdown', 'value'),
    Output('CupEquivalentUnit-dropdown', 'value'),
    Output('price-category-dropdown', 'value'),
    Input('clear-filters', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return [], None, None

# JavaScript for theme toggle
app.clientside_callback(
    """
    function(n_clicks) {
        const htmlEl = document.documentElement;
        const currentTheme = htmlEl.getAttribute('data-mantine-color-scheme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlEl.setAttribute('data-mantine-color-scheme', newTheme);
        return window.dash_clientside.no_update;
    }
    """,
    Output('color-scheme-toggle', 'n_clicks'),
    Input('color-scheme-toggle', 'n_clicks')
)

if __name__ == "__main__":
    app.run(debug=True, port=6070)