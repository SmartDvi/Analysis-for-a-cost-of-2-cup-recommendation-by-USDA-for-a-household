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
                                    "🍎 Fruit & Vegetable Cost Calculator",
                                    order=1,
                                    c='white',
                                    size='h2',
                                    fw=800,
                                ),
                                dmc.Text(
                                    "Calculate actual costs to meet USDA recommendations",
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
                                    DashIconify(icon="mdi:shopping", width=24, color=colors['success']),
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
                                        dmc.Text("Avg Cost/Edible Cup", size='xs', c='white', opacity=0.8),
                                        dmc.Title(f"${summary_stats['avg_actual_cost']:.2f}", order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:percent", width=24, color=colors['secondary']),
                                    dmc.Stack([
                                        dmc.Text("Avg Edible Yield", size='xs', c='white', opacity=0.8),
                                        dmc.Title(f"{summary_stats['avg_yield']:.1f}%", order=4, c='white')
                                    ], gap=0)
                                ], gap='sm')
                            ],
                            p='md',
                            style={'background': 'rgba(255,255,255,0.1)', 'borderRadius': '8px', 'flex': 1}
                        ),
                        dmc.Paper(
                            [
                                dmc.Group([
                                    DashIconify(icon="mdi:trending-down", width=24, color=colors['primary']),
                                    dmc.Stack([
                                        dmc.Text("Most Affordable", size='xs', c='white', opacity=0.8),
                                        dmc.Title(summary_stats['lowest_cost_item'], order=4, c='white', size='sm')
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
                            label='Select Fruits/Vegetables',
                            placeholder='Choose items...',
                            data=[{'value': fruit, 'label': fruit} for fruit in sorted(df['Fruit'].unique())],
                            value=[],
                            style={'width': 250},
                            clearable=True,
                            searchable=True,
                        ),
                        dmc.Select(
                            id='form-dropdown',
                            label='Form',
                            placeholder='All forms',
                            data=[{'value': form, 'label': form} for form in sorted(df['Form'].unique())],
                            value=None,
                            style={'width': 200},
                            clearable=True,
                        ),
                        dmc.Select(
                            id='price-category-dropdown',
                            label='Price Category',
                            placeholder='All categories',
                            data=[{'value': cat, 'label': cat} for cat in sorted(df['PriceCategory'].cat.categories)],
                            value=None,
                            style={'width': 200},
                            clearable=True,
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
                        dmc.Title("Household Calculator", order=4, c=colors['text_primary']),
                        DashIconify(icon="mdi:calculator", width=24, color=colors['primary'])
                    ],
                    justify='space-between'
                ),
                dmc.Text(
                    "Calculate your household's fruit & vegetable costs",
                    size='sm', c=colors['text_secondary']
                ),
                dmc.Divider(),

                # Household configuration
                dmc.Stack(
                    [
                        dmc.NumberInput(
                            id='adults-input',
                            label='Adults (19-50 years)',
                            min=0,
                            max=10,
                            value=2,
                            description='USDA: 4-5 cups daily',
                            leftSection=DashIconify(icon="mdi:account"),
                            style={'width': '100%'}
                        ),
                        dmc.NumberInput(
                            id='children-input',
                            label='Children (4-13 years)',
                            min=0,
                            max=10,
                            value=2,
                            description='USDA: 3-4 cups daily',
                            leftSection=DashIconify(icon="mdi:account-child"),
                            style={'width': '100%'}
                        ),
                        dmc.NumberInput(
                            id='teens-input',
                            label='Teens (14-18 years)',
                            min=0,
                            max=10,
                            value=0,
                            description='USDA: 4.5-5.5 cups daily',
                            leftSection=DashIconify(icon="mdi:account-supervisor"),
                            style={'width': '100%'}
                        ),
                    ],
                    gap='sm'
                ),

                # Budget preference
                dmc.Stack(
                    [
                        dmc.Select(
                            id='budget-tier',
                            label='Budget Preference',
                            value='avg',
                            data=[
                                {'value': 'low', 'label': 'Low Budget'},
                                {'value': 'avg', 'label': 'Average'},
                                {'value': 'high', 'label': 'High Budget'}
                            ],
                            leftSection=DashIconify(icon="mdi:currency-usd"),
                            style={'width': '100%'}
                        ),
                        dmc.Select(
                            id='period-selector-calc',
                            label='Time Period',
                            value='Yearly',
                            data=[
                                {'value': 'Daily', 'label': 'Daily'},
                                {'value': 'Weekly', 'label': 'Weekly'},
                                {'value': 'Monthly', 'label': 'Monthly'},
                                {'value': 'Yearly', 'label': 'Yearly'}
                            ],
                            leftSection=DashIconify(icon="mdi:calendar"),
                            style={'width': '100%'}
                        ),
                    ],
                    gap='sm'
                ),

                dmc.Button(
                    "Calculate Cost",
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

    if any(x in col.lower() for x in ['cost']):
        col_def['type'] = 'numericColumn'
        col_def['valueFormatter'] = {'function': 'd3.format("$,.2f")(params.value)'}
    elif any(x in col.lower() for x in ['cups', 'members']):
        col_def['type'] = 'numericColumn'
        col_def['valueFormatter'] = {'function': 'd3.format(".1f")(params.value)'}

    column_defs.append(col_def)

# Price categories tabs
price_categories_tabs = dmc.Paper(
    p=0,
    mb='xl',
    style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["card_border"]}',
        'borderRadius': '8px'
    },
    children=dmc.Tabs(
        children=[
            dmc.TabsList(
                children=[
                    dmc.TabsTab(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd-off", width=18),
                            dmc.Text("Low Budget", size='sm')
                        ], gap='xs'),
                        value='low-budget'
                    ),
                    dmc.TabsTab(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd", width=18),
                            dmc.Text("Budget", size='sm')
                        ], gap='xs'),
                        value='budget'
                    ),
                    dmc.TabsTab(
                        dmc.Group([
                            DashIconify(icon="mdi:currency-usd-circle", width=18),
                            dmc.Text("Moderate", size='sm')
                        ], gap='xs'),
                        value='moderate'
                    ),
                    dmc.TabsTab(
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
                        dmc.Badge(f"${price_benchmarks['low']:.2f}/cup", color="green", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced in lowest 25% - most affordable options",
                        size='sm', c=colors['text_secondary']
                    ),
                    dmc.Divider(),
                    dcc.Graph(
                        id='low-budget-chart',
                        figure=create_category_analysis('Low Budget'),
                        style={'height': 400}
                    )
                ], gap='md'),
                value='low-budget'
            ),

            # Budget Tab
            dmc.TabsPanel(
                dmc.Stack([
                    dmc.Group([
                        dmc.Title("Budget Analysis", order=3, c=colors['text_primary']),
                        dmc.Badge(f"${price_benchmarks['budget']:.2f}/cup", color="blue", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced 25-50% - good value for money",
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
                        dmc.Badge(f"${price_benchmarks['moderate']:.2f}/cup", color="orange", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items priced 50-75% - premium quality options",
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
                        dmc.Badge(f"${price_benchmarks['high']:.2f}/cup", color="red", size='lg')
                    ], justify='space-between'),
                    dmc.Text(
                        "Items in highest 25% - premium and specialty items",
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
        orientation='horizontal',
        id='price-tabs'
    )
)

# Cost summary section
cost_summary_section = dmc.Paper(
    p='md',
    mb='xl',
    style={
        'background': colors['card_bg'],
        'border': f'1px solid {colors["card_border"]}',
        'borderRadius': '8px'
    },
    children=[
        dmc.Stack([
            dmc.Group([
                dmc.Title("Annual Cost Summary", order=3, c=colors['text_primary']),
                dmc.Select(
                    id='period-selector-summary',
                    value='Yearly',
                    data=['Daily', 'Weekly', 'Monthly', 'Yearly'],
                    style={'width': 150}
                )
            ], justify='space-between'),
            dmc.Text(
                "Cost to meet USDA daily recommendations for different household types",
                size='sm', c=colors['text_secondary']
            ),
            dmc.Divider(),
            dcc.Graph(
                id='cost-summary-chart',
                figure=create_cost_summary(),
                style={'height': 500}
            )
        ], gap='md')
    ]
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

                # Yield Impact Visualization
                dmc.Paper(
                    p='md',
                    mb='xl',
                    style={
                        'background': colors['card_bg'],
                        'border': f'1px solid {colors["card_border"]}',
                        'borderRadius': '8px'
                    },
                    children=[
                        dmc.Title("Impact of Edible Yield on Costs", order=3, mb='md'),
                        dmc.Text(
                            "How much edible yield affects the actual cost per cup",
                            size='sm', c=colors['text_secondary'], mb='md'
                        ),
                        dcc.Graph(
                            id='yield-analysis',
                            figure=create_yield_analysis(),
                            style={'height': 500}
                        )
                    ]
                ),

                # Price comparison
                dmc.Paper(
                    p='md',
                    mb='xl',
                    style={
                        'background': colors['card_bg'],
                        'border': f'1px solid {colors["card_border"]}',
                        'borderRadius': '8px'
                    },
                    children=[
                        dmc.Title("Retail Price vs Actual Edible Cost", order=3, mb='md'),
                        dmc.Text(
                            "Comparing retail prices to actual costs per edible cup (accounting for yield)",
                            size='sm', c=colors['text_secondary'], mb='md'
                        ),
                        dcc.Graph(
                            id='price-comparison',
                            figure=create_price_comparison(),
                            style={'height': 500}
                        )
                    ]
                ),

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
                                            dmc.Title("Actual Cost Distribution", order=3, mb='md'),
                                            dmc.Text(
                                                "Distribution of actual costs per edible cup (yield-adjusted)",
                                                size='sm', c=colors['text_secondary'], mb='md'
                                            ),
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

                                    # Cost summary
                                    cost_summary_section,

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
                                                        f"{len(household_costs_df)} Household Types",
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

                # Footer with data sources
                dmc.Center(
                    dmc.Stack([
                        dmc.Text(
                            [
                                "Dashboard developed with ",
                                dmc.Text("Plotly Dash", c=colors['primary'], fw=600),
                                " • Dataset: Fruit and Vegetables Price Data"
                            ],
                            size='sm',
                            c=colors['text_secondary']
                        ),
                        dmc.Text(
                            [
                                "USDA Recommendations Source: ",
                                dmc.Text("MyPlate Dietary Guidelines 2020-2025", c=colors['secondary'], fw=600),
                                " • All costs are per edible cup (yield-adjusted)"
                            ],
                            size='xs',
                            c=colors['text_light']
                        )
                    ], gap=0, mt='xl', mb='md')
                )
            ]
        )
    ]
)

# Callbacks
@callback(
    Output('price-distribution-chart', 'figure'),
    Output('household-cost-chart', 'figure'),
    Output('yield-analysis', 'figure'),
    Output('price-comparison', 'figure'),
    Output('cost-summary-chart', 'figure'),
    Input('fruit-dropdown', 'value'),
    Input('form-dropdown', 'value'),
    Input('price-category-dropdown', 'value'),
    Input('period-selector', 'value'),
    Input('period-selector-summary', 'value')
)
def update_charts(fruits, form, price_category, period, summary_period):
    # Filter data
    filtered_df = df.copy()

    if fruits:
        filtered_df = filtered_df[filtered_df['Fruit'].isin(fruits)]
    if form:
        filtered_df = filtered_df[filtered_df['Form'] == form]
    if price_category:
        filtered_df = filtered_df[filtered_df['PriceCategory'] == price_category]

    # Update price distribution with filtered data
    fig1 = create_price_distribution()
    if len(filtered_df) > 0:
        # Update the entire figure for filtered data
        fig1 = go.Figure()
        fig1.add_trace(go.Histogram(
            x=filtered_df['ActualCostPerCup'],
            nbinsx=40,
            name='Cost Distribution',
            marker_color=colors['primary'],
            opacity=0.7,
            histnorm='probability density'
        ))
        
        # Add KDE curve for filtered data
        if len(filtered_df) > 1:
            kde = stats.gaussian_kde(filtered_df['ActualCostPerCup'].dropna())
            x_range = np.linspace(filtered_df['ActualCostPerCup'].min(), 
                                 filtered_df['ActualCostPerCup'].max(), 100)
            y_range = kde(x_range)
            
            fig1.add_trace(go.Scatter(
                x=x_range, y=y_range,
                mode='lines',
                name='Density',
                line=dict(color=colors['danger'], width=2),
                yaxis='y2'
            ))

        # Update layout
        fig1.update_layout(
            title='Filtered Cost Distribution',
            xaxis_title='Cost per Edible Cup ($)',
            yaxis_title='Frequency',
            yaxis2=dict(
                title='Density',
                overlaying='y',
                side='right',
                showgrid=False
            ),
            hovermode='x unified',
            plot_bgcolor=colors['card_bg'],
            paper_bgcolor=colors['background'],
            font=dict(color=colors['text_primary']),
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )

    # Update household cost comparison
    fig2 = create_household_cost_comparison(period)
    
    # Update yield analysis
    fig3 = create_yield_analysis()
    if len(filtered_df) > 0:
        fig3.data[0].x = filtered_df['Yield'] * 100
        fig3.data[0].y = filtered_df['ActualCostPerCup']
        fig3.data[0].customdata = np.column_stack((
            filtered_df['RetailPrice'],
            filtered_df['RetailPriceUnit'],
            filtered_df['CupEquivalentSize'],
            filtered_df['CupEquivalentUnit']
        ))
    
    # Update price comparison
    fig4 = create_price_comparison()
    if len(filtered_df) > 0:
        # Get top 15 most affordable from filtered data
        sorted_filtered = filtered_df.sort_values('ActualCostPerCup').head(15)
        if len(sorted_filtered) > 0:
            fig4.data[0].x = sorted_filtered['Fruit']
            fig4.data[0].y = sorted_filtered['RetailPrice']
            fig4.data[1].x = sorted_filtered['Fruit']
            fig4.data[1].y = sorted_filtered['ActualCostPerCup']
            fig4.data[0].customdata = np.column_stack((
                sorted_filtered['Form'],
                sorted_filtered['RetailPriceUnit']
            ))
            fig4.data[1].customdata = np.column_stack((
                sorted_filtered['Form'],
                sorted_filtered['Yield'] * 100
            ))
    
    # Update cost summary
    fig5 = create_cost_summary()
    # Update period in cost summary if needed
    if summary_period != 'Yearly':
        period_map = {'Daily': 1, 'Weekly': 7, 'Monthly': 30, 'Yearly': 365}
        multiplier = period_map.get(summary_period, 365)
        
        # Update the bars for the new period
        for i, tier in enumerate(['low', 'avg', 'high']):
            costs = household_costs_df[f'{tier}_Yearly_Cost'] / 365 * multiplier
            fig5.data[i].y = costs.values
            fig5.data[i].text = costs.apply(lambda x: f'${x:,.0f}').values
        
        fig5.update_layout(
            title=f'{summary_period} Cost to Meet USDA Recommendations',
            yaxis_title=f'{summary_period} Cost ($)'
        )

    return fig1, fig2, fig3, fig4, fig5

@callback(
    Output('cost-estimate-results', 'children'),
    Input('get-cost-estimate-btn', 'n_clicks'),
    State('adults-input', 'value'),
    State('children-input', 'value'),
    State('teens-input', 'value'),
    State('budget-tier', 'value'),
    State('period-selector-calc', 'value')
)
def calculate_cost_estimate(n_clicks, adults, children, teens, budget_tier, period):
    if n_clicks is None:
        return dmc.Alert(
            "Configure your household and click 'Calculate Cost' to see results",
            color="blue",
            variant="light"
        )

    # Calculate USDA daily cups needed
    adult_cups = 4.5  # Average for adults
    child_cups = 3.5  # Average for children
    teen_cups = 5.0   # Average for teens
    
    daily_cups_needed = (adults * adult_cups) + (children * child_cups) + (teens * teen_cups)
    
    # Get price for selected budget tier
    price = price_benchmarks[budget_tier]
    
    # Calculate costs for different periods
    period_map = {'Daily': 1, 'Weekly': 7, 'Monthly': 30, 'Yearly': 365}
    multiplier = period_map.get(period, 365)
    
    period_cost = daily_cups_needed * price * multiplier

    return dmc.Stack([
        dmc.Group([
            dmc.Paper([
                dmc.Text("Daily Cups Needed", size='xs', c=colors['text_secondary']),
                dmc.Title(f"{daily_cups_needed:.1f} cups", order=4, c=colors['text_primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
            dmc.Paper([
                dmc.Text(f"Cost per Cup ({budget_tier.title()})", size='xs', c=colors['text_secondary']),
                dmc.Title(f"${price:.2f}", order=4, c=colors['primary'])
            ], p='md', style={'flex': 1, 'background': colors['background'], 'borderRadius': '8px'}),
        ], grow=True),
        dmc.Paper([
            dmc.Group([
                DashIconify(icon="mdi:calendar", width=20, color=colors['primary']),
                dmc.Stack([
                    dmc.Text(f"{period} Cost", size='xs', c=colors['text_secondary']),
                    dmc.Title(f"${period_cost:.2f}", order=3, c=colors['text_primary'])
                ], gap=0)
            ], gap='sm')
        ], p='md', style={'background': colors['background'], 'borderRadius': '8px'}),
        dmc.Alert(
            [
                dmc.Text(f"Your household needs:", fw=500),
                html.Br(),
                dmc.Text(f"• {adults} adult(s): {adults * adult_cups:.1f} cups daily"),
                html.Br(),
                dmc.Text(f"• {children} child(ren): {children * child_cups:.1f} cups daily"),
                html.Br() if teens > 0 else html.Div(),
                dmc.Text(f"• {teens} teen(s): {teens * teen_cups:.1f} cups daily") if teens > 0 else html.Div(),
                html.Br(),
                dmc.Text(f"Total: {daily_cups_needed:.1f} cups daily to meet USDA recommendations")
            ],
            title="Cost Summary",
            color="green",
            variant="light"
        )
    ], gap='sm')

@callback(
    Output('fruit-dropdown', 'value'),
    Output('form-dropdown', 'value'),
    Output('price-category-dropdown', 'value'),
    Input('clear-filters', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return [], None, None

# Callback for tab charts
@callback(
    Output('low-budget-chart', 'figure'),
    Output('budget-chart', 'figure'),
    Output('moderate-chart', 'figure'),
    Output('high-budget-chart', 'figure'),
    Input('price-tabs', 'value'),
    Input('fruit-dropdown', 'value'),
    Input('form-dropdown', 'value'),
    Input('price-category-dropdown', 'value')
)
def update_tab_charts(selected_tab, fruits, form, price_category):
    # Filter data based on dropdowns
    filtered_df = df.copy()
    
    if fruits:
        filtered_df = filtered_df[filtered_df['Fruit'].isin(fruits)]
    if form:
        filtered_df = filtered_df[filtered_df['Form'] == form]
    if price_category:
        filtered_df = filtered_df[filtered_df['PriceCategory'] == price_category]
    
    # Create figures for each category with filtered data
    low_budget_fig = create_category_analysis('Low Budget')
    budget_fig = create_category_analysis('Budget')
    moderate_fig = create_category_analysis('Moderate')
    high_budget_fig = create_category_analysis('High Budget')
    
    # Apply filters if data is filtered
    if len(filtered_df) > 0:
        for category, fig in [('Low Budget', low_budget_fig), 
                             ('Budget', budget_fig), 
                             ('Moderate', moderate_fig), 
                             ('High Budget', high_budget_fig)]:
            cat_df = filtered_df[filtered_df['PriceCategory'] == category]
            if len(cat_df) > 0:
                top_affordable = cat_df.nsmallest(10, 'ActualCostPerCup')
                if len(top_affordable) > 0:
                    fig.data[0].x = top_affordable['ActualCostPerCup']
                    fig.data[0].y = top_affordable['Fruit']
                    fig.data[0].customdata = np.column_stack((
                        top_affordable['Form'],
                        top_affordable['Yield'] * 100,
                        top_affordable['RetailPrice'],
                        top_affordable['RetailPriceUnit']
                    ))
    
    return low_budget_fig, budget_fig, moderate_fig, high_budget_fig

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