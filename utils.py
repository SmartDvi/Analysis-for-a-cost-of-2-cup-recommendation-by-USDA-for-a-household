import pandas as pd
import numpy as np
from numpy import median
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

# Enhanced color scheme with better accessibility
colors = {
    'background': "#f8fafc",
    'card_bg': "#ffffff",
    'card_border': '#e2e8f0',
    'primary': '#2563eb',
    'primary_light': '#3b82f6',
    'secondary': '#06b6d4',
    'secondary_light': '#22d3ee',
    'success': '#10b981',
    'success_light': '#34d399',
    'warning': '#f59e0b',
    'warning_light': '#fbbf24',
    'danger': '#ef4444',
    'danger_light': '#f87171',
    'text_primary': "#1e293b",
    'text_secondary': '#475569',
    'text_light': '#64748b',
    'accent_gradient': 'linear-gradient(135deg, #2563eb 0%, #06b6d4 100%)',
    'grid_line': '#e2e8f0',
    'divider': '#cbd5e1'
}

# Load and prepare data
df = pd.read_csv("C:\\Users\\Moving_King\\Downloads\\Fruit and Vegetables Price dataset - Sheet1.csv")

# Clean data
df['Form'] = df['Form'].fillna('Fresh')
df['CupEquivalentUnit'] = df['CupEquivalentUnit'].fillna('cup')
df['Fruit'] = df['Fruit'].str.title()

# Calculate key metrics
avg_cost = df['CupEquivalentPrice'].mean()
median_cost = df['CupEquivalentPrice'].median()

# Enhanced price categorization with quartiles
price_quartiles = df['CupEquivalentPrice'].quantile([0.25, 0.5, 0.75])
df['CupEquivalentPriceCategory'] = pd.cut(
    df['CupEquivalentPrice'],
    bins=[0, price_quartiles[0.25], price_quartiles[0.5], price_quartiles[0.75], float('inf')],
    labels=['Low Budget', 'Budget', 'Moderate', 'High Budget'],
    include_lowest=True
)

# Enhanced USDA recommendations with more detail
usda_recommendations = {
    'children_2-3': {'min': 1, 'max': 1.5, 'category': 'Children'},
    'children_4-8': {'min': 1.5, 'max': 2, 'category': 'Children'},
    'children_9-13': {'min': 2, 'max': 2.5, 'category': 'Children'},
    'girls_14-18': {'min': 1.5, 'max': 2, 'category': 'Teens'},
    'boys_14-18': {'min': 2, 'max': 2.5, 'category': 'Teens'},
    'women_19-30': {'min': 2, 'max': 2.5, 'category': 'Adults'},
    'women_31-50': {'min': 1.5, 'max': 2, 'category': 'Adults'},
    'women_51+': {'min': 1.5, 'max': 2, 'category': 'Adults'},
    'men_19-30': {'min': 2, 'max': 2.5, 'category': 'Adults'},
    'men_31-50': {'min': 2, 'max': 2.5, 'category': 'Adults'},
    'men_51+': {'min': 2, 'max': 2, 'category': 'Adults'}
}

# Enhanced household configurations with descriptions
household_types = {
    'single_adult': {
        'adults': 1, 'children': 0, 'teens': 0,
        #'description': 'Single working adult',
        'avg_daily_cups': 2.0
    },
    'couple': {
        'adults': 2, 'children': 0, 'teens': 0,
      #  'description': 'Dual-income couple',
        'avg_daily_cups': 4.0
    },
    'single_parent_1child': {
        'adults': 1, 'children': 1, 'teens': 0,
     #   'description': 'Single parent with young child',
        'avg_daily_cups': 3.25
    },
    'single_parent_2children': {
        'adults': 1, 'children': 2, 'teens': 0,
     #   'description': 'Single parent with two children',
        'avg_daily_cups': 4.5
    },
    'family_2plus2': {
        'adults': 2, 'children': 2, 'teens': 0,
     #   'description': 'Traditional family (2 adults, 2 children)',
        'avg_daily_cups': 6.5
    },
    'family_2plus3': {
        'adults': 2, 'children': 3, 'teens': 0,
     #   'description': 'Large family (2 adults, 3 children)',
        'avg_daily_cups': 7.75
    },
    'family_with_teens': {
        'adults': 2, 'children': 0, 'teens': 2,
     #   'description': 'Family with two teenagers',
        'avg_daily_cups': 7.5
    },
    'multi_generational': {
        'adults': 3, 'children': 2, 'teens': 1,
     #   'description': 'Multi-generational household',
        'avg_daily_cups': 10.25
    }
}

# Function to calculate daily cups needed with enhanced logic
def calculate_daily_cups(household_config):
    adults = household_config.get('adults', 0)
    children = household_config.get('children', 0)
    teens = household_config.get('teens', 0)

    # Enhanced calculation with different requirements
    adults_cups = 2.0  # Average for adults
    teens_cups = 1.75  # Slightly less than adults
    children_cups = 1.25  # Children need less

    return {
        'total': (adults * adults_cups) + (teens * teens_cups) + (children * children_cups),
        'fruit': (adults * 1.5) + (teens * 1.5) + (children * 1.0),
        'vegetable': (adults * 2.0) + (teens * 2.0) + (children * 1.0),
        'adults_cups': adults * adults_cups,
        'teens_cups': teens * teens_cups,
        'children_cups': children * children_cups
    }

# Calculate price benchmarks for different budgets
price_benchmarks = {
    'low': df[df['CupEquivalentPrice'] <= price_quartiles[0.25]]['CupEquivalentPrice'].mean(),
    'budget': df[df['CupEquivalentPrice'] <= price_quartiles[0.5]]['CupEquivalentPrice'].mean(),
    'moderate': df[df['CupEquivalentPrice'] <= price_quartiles[0.75]]['CupEquivalentPrice'].mean(),
    'high': df['CupEquivalentPrice'].max(),
    'avg': avg_cost
}

# Enhanced household cost calculations
def calculate_household_costs():
    household_costs = {}

    for household, config in household_types.items():
        cups_data = calculate_daily_cups(config)
        daily_cups_needed = cups_data['total']

        # Calculate for different time periods
        periods = {
            'daily': daily_cups_needed,
            'weekly': daily_cups_needed * 7,
            'monthly': daily_cups_needed * 30,
            'yearly': daily_cups_needed * 365
        }

        household_costs[household] = {
            'Household Type': household.replace('_', ' ').title(),
           # 'Description': config['description'],
            'Adults': config['adults'],
            'Children': config['children'],
            'Teens': config['teens'],
            'Total Members': config['adults'] + config['children'] + config['teens'],
            'Daily Cups Needed': daily_cups_needed,
            'Daily Fruit Cups': cups_data['fruit'],
            'Daily Vegetable Cups': cups_data['vegetable'],
        }

        # Add costs for each price tier and period
        for tier_name, tier_price in price_benchmarks.items():
            for period_name, period_multiplier in [('Daily', 1), ('Weekly', 7),
                                                  ('Monthly', 30), ('Yearly', 365)]:
                key = f'{tier_name}_{period_name}'
                household_costs[household][key] = daily_cups_needed * period_multiplier * tier_price

    return pd.DataFrame(household_costs).T

household_costs_df = calculate_household_costs()

# Create visualization functions
def create_price_distribution():
    """Create enhanced price distribution visualization"""
    fig = go.Figure()

    # Histogram with density curve
    fig.add_trace(go.Histogram(
        x=df['CupEquivalentPrice'],
        nbinsx=40,
        name='Price Distribution',
        marker_color=colors['primary'],
        opacity=0.7,
        histnorm='probability density'
    ))

    # Add KDE curve
    kde = stats.gaussian_kde(df['CupEquivalentPrice'].dropna())
    x_range = np.linspace(df['CupEquivalentPrice'].min(), df['CupEquivalentPrice'].max(), 100)
    y_range = kde(x_range)

    fig.add_trace(go.Scatter(
        x=x_range, y=y_range,
        mode='lines',
        name='Density',
        line=dict(color=colors['danger'], width=2),
        yaxis='y2'
    ))

    # Add vertical lines for key metrics
    metrics = [
        ('Min', df['CupEquivalentPrice'].min(), colors['success']),
        ('Q1', price_quartiles[0.25], colors['warning']),
        ('Median', median_cost, colors['primary']),
        ('Q3', price_quartiles[0.75], colors['warning']),
        ('Max', df['CupEquivalentPrice'].max(), colors['danger'])
    ]

    for name, value, color in metrics:
        fig.add_vline(
            x=value, line_dash="dash",
            line_color=color,
            annotation_text=f"{name}: ${value:.2f}",
            annotation_position="top right"
        )

    fig.update_layout(
        title='Fruit & Vegetable Price Distribution',
        xaxis_title='Price per Cup Equivalent ($)',
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

    return fig

def create_category_analysis(category='Low Budget'):
    """Create analysis for a specific price category"""
    category_df = df[df['CupEquivalentPriceCategory'] == category]

    fig = go.Figure()

    # Top 10 most affordable in this category
    top_affordable = category_df.nsmallest(10, 'CupEquivalentPrice')

    fig.add_trace(go.Bar(
        x=top_affordable['CupEquivalentPrice'],
        y=top_affordable['Fruit'],
        orientation='h',
        marker_color=colors['primary'],
        text=top_affordable['CupEquivalentPrice'].apply(lambda x: f'${x:.2f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Price: $%{x:.2f}<br>Form: %{customdata}<extra></extra>',
        customdata=top_affordable['Form']
    ))

    fig.update_layout(
        title=f'Top 10 Most Affordable - {category}',
        xaxis_title='Price per Cup Equivalent ($)',
        yaxis=dict(autorange='reversed'),
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        margin=dict(l=150, r=50, t=50, b=50)
    )

    return fig

def create_household_cost_comparison(period='Weekly'):
    """Create comparison of household costs"""
    cost_columns = [f'{tier}_{period}' for tier in price_benchmarks.keys()]

    fig = go.Figure()

    colors_tiers = [colors['success'], colors['primary'],
                    colors['warning'], colors['danger'], colors['secondary']]

    for i, (tier, color) in enumerate(zip(price_benchmarks.keys(), colors_tiers)):
        tier_costs = household_costs_df[f'{tier}_{period}'].values

        fig.add_trace(go.Bar(
            x=household_costs_df['Household Type'],
            y=tier_costs,
            name=tier.title(),
            marker_color=color,
            hovertemplate=f'<b>%{{x}}</b><br>{tier.title()}: $%{{y:.2f}}<extra></extra>',
            text=[f'${x:.0f}' for x in tier_costs],
            textposition='outside'
        ))

    fig.update_layout(
        title=f'Hourly Costs by Household Type ({period})',
        xaxis_title='Household Type',
        yaxis_title=f'Cost ($)',
        barmode='group',
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        hovermode='x unified',
        xaxis=dict(tickangle=45)
    )

    return fig

def create_affordability_matrix():
    """Create matrix showing affordability across categories"""
    matrix_df = df.groupby(['Form', 'CupEquivalentPriceCategory']).agg({
        'CupEquivalentPrice': ['mean', 'count']
    }).round(2).reset_index()

    matrix_df.columns = ['Form', 'Category', 'Avg_Price', 'Count']

    fig = px.scatter(
        matrix_df,
        x='Form',
        y='Category',
        size='Count',
        color='Avg_Price',
        color_continuous_scale='RdYlGn_r',
        size_max=60,
        hover_data=['Avg_Price', 'Count'],
        labels={'Avg_Price': 'Average Price ($)'}
    )

    fig.update_layout(
        title='Affordability Matrix: Form vs Price Category',
        xaxis_title='Form',
        yaxis_title='Price Category',
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        coloraxis_colorbar=dict(
            title="Avg Price ($)",
            thickness=20,
            len=0.5
        )
    )

    return fig

# Create summary statistics
summary_stats = {
    'total_items': len(df),
    'unique_fruits': df['Fruit'].nunique(),
    'avg_price': avg_cost,
    'median_price': median_cost,
    'price_range': f"${df['CupEquivalentPrice'].min():.2f} - ${df['CupEquivalentPrice'].max():.2f}",
    'budget_items': len(df[df['CupEquivalentPriceCategory'] == 'Low Budget']),
    'premium_items': len(df[df['CupEquivalentPriceCategory'] == 'High Budget'])
}