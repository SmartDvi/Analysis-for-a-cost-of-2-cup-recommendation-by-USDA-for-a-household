import pandas as pd
import numpy as np
from numpy import median
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

# Enhanced color scheme
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

# Calculate the actual price per edible cup
# IMPORTANT: Based on the dataset structure, CupEquivalentPrice appears to be price per cup equivalent
# We need to check if it accounts for yield. Let's verify the calculation:
# For Apples Fresh: RetailPrice = $1.8541 per pound, CupEquivalentSize = 0.2425 pounds
# Without yield: 1.8541 * 0.2425 = $0.4496
# With 90% yield: 0.4496 / 0.90 = $0.4996 (matches dataset)
# So CupEquivalentPrice ALREADY accounts for yield!

print("Verification calculation for Apples (Fresh):")
print(f"Retail Price: ${df.loc[0, 'RetailPrice']:.4f} per {df.loc[0, 'RetailPriceUnit']}")
print(f"Cup Equivalent Size: {df.loc[0, 'CupEquivalentSize']} {df.loc[0, 'CupEquivalentUnit']}")
print(f"Theoretical price without yield: ${df.loc[0, 'RetailPrice'] * df.loc[0, 'CupEquivalentSize']:.4f}")
print(f"Dataset CupEquivalentPrice: ${df.loc[0, 'CupEquivalentPrice']:.4f}")
print(f"Yield: {df.loc[0, 'Yield']*100}%")

# Key finding: CupEquivalentPrice = (RetailPrice * CupEquivalentSize) / Yield
# So CupEquivalentPrice already represents the ACTUAL cost per edible cup!

# Let's verify this formula for a few entries
df['CalculatedCupEquivalentPrice'] = (df['RetailPrice'] * df['CupEquivalentSize']) / df['Yield']
df['PriceCheck'] = abs(df['CalculatedCupEquivalentPrice'] - df['CupEquivalentPrice']) < 0.01

print(f"\nPrice calculation matches dataset for {df['PriceCheck'].sum()}/{len(df)} items")

# Since CupEquivalentPrice already accounts for yield, we'll use it directly
df['ActualCostPerCup'] = df['CupEquivalentPrice']

# Calculate key metrics
avg_cost = df['ActualCostPerCup'].mean()
median_cost = df['ActualCostPerCup'].median()

# Enhanced price categorization with quartiles
price_quartiles = df['ActualCostPerCup'].quantile([0.25, 0.5, 0.75])
df['PriceCategory'] = pd.cut(
    df['ActualCostPerCup'],
    bins=[0, price_quartiles[0.25], price_quartiles[0.5], price_quartiles[0.75], float('inf')],
    labels=['Low Budget', 'Budget', 'Moderate', 'High Budget'],
    include_lowest=True
)

# USDA daily cup recommendations (MINIMUM requirements for health)
# Source: USDA MyPlate Dietary Guidelines 2020-2025
# These are the MINIMUM daily servings for optimal health
usda_daily_minimums = {
    'children_2-3': {'fruit': 1, 'vegetable': 1, 'total': 2},
    'children_4-8': {'fruit': 1.5, 'vegetable': 1.5, 'total': 3},
    'children_9-13': {'fruit': 2, 'vegetable': 2, 'total': 4},
    'girls_14-18': {'fruit': 2, 'vegetable': 2.5, 'total': 4.5},
    'boys_14-18': {'fruit': 2.5, 'vegetable': 3, 'total': 5.5},
    'women_19-30': {'fruit': 2, 'vegetable': 2.5, 'total': 4.5},
    'women_31-50': {'fruit': 1.5, 'vegetable': 2.5, 'total': 4},
    'women_51+': {'fruit': 1.5, 'vegetable': 2, 'total': 3.5},
    'men_19-30': {'fruit': 2, 'vegetable': 3, 'total': 5},
    'men_31-50': {'fruit': 2, 'vegetable': 3, 'total': 5},
    'men_51+': {'fruit': 2, 'vegetable': 2.5, 'total': 4.5}
}

# Household configurations (examples for analysis)
# Using USDA minimums for different age groups
household_types = {
    'single_adult': {
        'adults': 1, 
        'age_group': '31-50', 
        'gender': 'men',
        'description': 'Single Adult',
        'usda_daily_cups': 5.0,  # USDA minimum for men 31-50
        'fruit_cups': 2.0,
        'vegetable_cups': 2.5,
        'members': ['men_31-50']
    },
    'couple_no_kids': {
        'adults': 2, 
        'age_group': '31-50', 
        'gender_mix': ['men', 'women'],
        'description': 'Couple (No Children)',
        'usda_daily_cups': 9.0,  # 5 (men) + 4 (women)
        'fruit_cups': 3.5,       # 2 + 1.5
        'vegetable_cups': 5,   # 2.5 + 2.5
        'members': ['men_31-50', 'women_31-50']
    },
    'family_2adults_2children': {
        'adults': 2, 
        'children': 2, 
        'adult_age': '31-50', 
        'child_ages': ['4-8', '9-13'],
        'description': 'Family (2 Adults, 2 Children)',
        'usda_daily_cups': 14.0,  # 5 + 4 + 3 + 2
        'fruit_cups': 5.5,        # 2 + 1.5 + 1.5 + 0.5
        'vegetable_cups': 8,    # 2.5 + 2.5 + 1.5 + 1.5
        'members': ['men_31-50', 'women_31-50', 'children_4-8', 'children_9-13']
    },
    'single_parent_2children': {
        'adults': 1, 
        'children': 2, 
        'adult_age': '31-50', 
        'child_ages': ['4-8', '9-13'],
        'description': 'Single Parent (2 Children)',
        'usda_daily_cups': 9.0,   # 4 + 3 + 2
        'fruit_cups': 3.5,        # 1.5 + 1.5 + 0.5
        'vegetable_cups': 5.5,    # 2.5 + 1.5 + 1.5
        'members': ['women_31-50', 'children_4-8', 'children_9-13']
    }
}

# Calculate price benchmarks for different budgets
price_benchmarks = {
    'low': df[df['PriceCategory'] == 'Low Budget']['ActualCostPerCup'].mean(),
    'budget': df[df['PriceCategory'] == 'Budget']['ActualCostPerCup'].mean(),
    'moderate': df[df['PriceCategory'] == 'Moderate']['ActualCostPerCup'].mean(),
    'high': df[df['PriceCategory'] == 'High Budget']['ActualCostPerCup'].mean(),
    'avg': avg_cost,
    'min': df['ActualCostPerCup'].min(),
    'max': df['ActualCostPerCup'].max()
}

# Household cost calculations
def calculate_household_costs():
    """Calculate costs for different household types"""
    household_costs = {}

    for household, config in household_types.items():
        daily_cups_needed = config['usda_daily_cups']
        
        household_costs[household] = {
            'Household Type': config['description'],
            'USDA Daily Cups': daily_cups_needed,
            'Fruit Cups Daily': config['fruit_cups'],
            'Vegetable Cups Daily': config['vegetable_cups'],
            'Total Members': len(config['members'])
        }

        # Add costs for each price tier and period
        for tier_name, tier_price in price_benchmarks.items():
            if tier_name in ['low', 'budget', 'moderate', 'high', 'avg']:
                daily_cost = daily_cups_needed * tier_price
                
                household_costs[household].update({
                    f'{tier_name}_Daily_Cost': daily_cost,
                    f'{tier_name}_Weekly_Cost': daily_cost * 7,
                    f'{tier_name}_Monthly_Cost': daily_cost * 30,
                    f'{tier_name}_Yearly_Cost': daily_cost * 365,
                })

    return pd.DataFrame(household_costs).T

household_costs_df = calculate_household_costs()

# Create visualization functions
def create_yield_analysis():
    """Visualize how yield affects the relationship between retail price and actual cost"""
    
    fig = go.Figure()
    
    # Scatter plot: Yield vs Actual Cost
    fig.add_trace(go.Scatter(
        x=df['Yield'] * 100,  # Convert to percentage
        y=df['ActualCostPerCup'],
        mode='markers',
        marker=dict(
            size=10,
            color=df['ActualCostPerCup'],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="Actual Cost ($)")
        ),
        text=df['Fruit'] + ' (' + df['Form'] + ')',
        hovertemplate='<b>%{text}</b><br>' +
                      'Edible Yield: %{x:.1f}%<br>' +
                      'Retail Price: $%{customdata[0]:.2f}/{customdata[1]}<br>' +
                      'Actual Cost: $%{y:.2f}/cup<br>' +
                      'Cup Equivalent: %{customdata[2]:.3f} {customdata[3]}<extra></extra>',
        customdata=np.column_stack((
            df['RetailPrice'],
            df['RetailPriceUnit'],
            df['CupEquivalentSize'],
            df['CupEquivalentUnit']
        ))
    ))
    
    # Add average yield line
    avg_yield = df['Yield'].mean() * 100
    fig.add_vline(
        x=avg_yield, line_dash="dash",
        line_color=colors['primary'],
        annotation_text=f"Average Yield: {avg_yield:.1f}%",
        annotation_position="top right"
    )
    
    fig.update_layout(
        title='Impact of Edible Yield on Actual Food Costs',
        xaxis_title='Edible Yield (%)',
        yaxis_title='Actual Cost per Edible Cup ($)',
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        hovermode='closest'
    )
    
    return fig

def create_cost_summary():
    """Create summary of annual costs across households"""
    
    fig = go.Figure()
    
    households = household_costs_df['Household Type']
    
    # Add bars for yearly costs at different budget levels
    fig.add_trace(go.Bar(
        name='Low Budget',
        x=households,
        y=household_costs_df['low_Yearly_Cost'],
        marker_color=colors['success'],
        text=household_costs_df['low_Yearly_Cost'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                     'Low Budget: $%{y:,.0f}/year<br>' +
                     'Daily Cups Needed: %{customdata}<extra></extra>',
        customdata=household_costs_df['USDA Daily Cups'].apply(lambda x: f'{x:.1f}')
    ))
    
    fig.add_trace(go.Bar(
        name='Average Cost',
        x=households,
        y=household_costs_df['avg_Yearly_Cost'],
        marker_color=colors['primary'],
        text=household_costs_df['avg_Yearly_Cost'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Average: $%{y:,.0f}/year<extra></extra>'
    ))
    
    fig.add_trace(go.Bar(
        name='High Budget',
        x=households,
        y=household_costs_df['high_Yearly_Cost'],
        marker_color=colors['warning'],
        text=household_costs_df['high_Yearly_Cost'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>High Budget: $%{y:,.0f}/year<extra></extra>'
    ))
    
    fig.update_layout(
        title='Annual Cost to Meet USDA Recommendations',
        xaxis_title='Household Type',
        yaxis_title='Annual Cost ($)',
        barmode='group',
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        xaxis=dict(tickangle=45),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )
    
    return fig

def create_price_distribution():
    """Create price distribution visualization"""
    fig = go.Figure()

    # Histogram with density curve
    fig.add_trace(go.Histogram(
        x=df['ActualCostPerCup'],
        nbinsx=40,
        name='Cost Distribution',
        marker_color=colors['primary'],
        opacity=0.7,
        histnorm='probability density'
    ))

    # Add KDE curve
    kde = stats.gaussian_kde(df['ActualCostPerCup'].dropna())
    x_range = np.linspace(df['ActualCostPerCup'].min(), 
                         df['ActualCostPerCup'].max(), 100)
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
        ('Min', df['ActualCostPerCup'].min(), colors['success']),
        ('Q1', price_quartiles[0.25], colors['warning']),
        ('Median', median_cost, colors['primary']),
        ('Q3', price_quartiles[0.75], colors['warning']),
        ('Max', df['ActualCostPerCup'].max(), colors['danger'])
    ]

    for name, value, color in metrics:
        fig.add_vline(
            x=value, line_dash="dash",
            line_color=color,
            annotation_text=f"{name}: ${value:.2f}",
            annotation_position="top right"
        )

    fig.update_layout(
        title='Actual Cost per Edible Cup Distribution',
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

    return fig

def create_category_analysis(category='Low Budget'):
    """Create analysis for a specific price category"""
    category_df = df[df['PriceCategory'] == category]

    fig = go.Figure()

    # Top 10 most affordable in this category
    top_affordable = category_df.nsmallest(10, 'ActualCostPerCup')

    fig.add_trace(go.Bar(
        x=top_affordable['ActualCostPerCup'],
        y=top_affordable['Fruit'],
        orientation='h',
        marker_color=colors['primary'],
        text=top_affordable['ActualCostPerCup'].apply(lambda x: f'${x:.2f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>' +
                      'Form: %{customdata[0]}<br>' +
                      'Actual Cost: $%{x:.2f}/cup<br>' +
                      'Yield: %{customdata[1]:.0f}%<br>' +
                      'Retail: $%{customdata[2]:.2f}/{customdata[3]}<extra></extra>',
        customdata=np.column_stack((
            top_affordable['Form'],
            top_affordable['Yield'] * 100,
            top_affordable['RetailPrice'],
            top_affordable['RetailPriceUnit']
        ))
    ))

    fig.update_layout(
        title=f'Top 10 Most Affordable - {category}',
        xaxis_title='Actual Cost per Edible Cup ($)',
        yaxis=dict(autorange='reversed'),
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        margin=dict(l=150, r=50, t=50, b=50)
    )

    return fig

def create_household_cost_comparison(period='Weekly'):
    """Create comparison of household costs"""
    period_map = {'Daily': 1, 'Weekly': 7, 'Monthly': 30, 'Yearly': 365}
    multiplier = period_map.get(period, 7)
    
    fig = go.Figure()

    colors_tiers = [colors['success'], colors['primary'], colors['warning']]

    for i, (tier, color) in enumerate(zip(['low', 'avg', 'high'], colors_tiers)):
        # Calculate costs for this period
        costs = []
        for household in household_types.keys():
            daily_cups = household_types[household]['usda_daily_cups']
            period_cost = daily_cups * price_benchmarks[tier] * multiplier
            costs.append(period_cost)

        fig.add_trace(go.Bar(
            x=[household_types[h]['description'] for h in household_types.keys()],
            y=costs,
            name=f'{tier.title()} Budget',
            marker_color=color,
            hovertemplate=f'<b>%{{x}}</b><br>{tier.title()}: $%{{y:.2f}}<br>' +
                         'Daily Cups: %{customdata}<extra></extra>',
            customdata=[f"{household_types[h]['usda_daily_cups']:.1f}" 
                       for h in household_types.keys()],
            text=[f'${x:.0f}' for x in costs],
            textposition='outside'
        ))

    fig.update_layout(
        title=f'Hourly Costs ({period})',
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

def create_price_comparison():
    """Compare retail price vs actual cost per cup"""
    
    fig = go.Figure()
    
    # Sort by actual cost
    sorted_df = df.sort_values('ActualCostPerCup').head(15)
    
    fig.add_trace(go.Bar(
        name='Retail Price (per unit)',
        x=sorted_df['Fruit'],
        y=sorted_df['RetailPrice'],
        marker_color=colors['secondary'],
        text=sorted_df['RetailPrice'].apply(lambda x: f'${x:.2f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                     'Form: %{customdata[0]}<br>' +
                     'Retail Price: $%{y:.2f}/%{customdata[1]}<extra></extra>',
        customdata=np.column_stack((
            sorted_df['Form'],
            sorted_df['RetailPriceUnit']
        ))
    ))
    
    fig.add_trace(go.Bar(
        name='Actual Cost (per edible cup)',
        x=sorted_df['Fruit'],
        y=sorted_df['ActualCostPerCup'],
        marker_color=colors['primary'],
        text=sorted_df['ActualCostPerCup'].apply(lambda x: f'${x:.2f}'),
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>' +
                     'Form: %{customdata[0]}<br>' +
                     'Actual Cost: $%{y:.2f}/cup<br>' +
                     'Yield: %{customdata[1]:.0f}%<extra></extra>',
        customdata=np.column_stack((
            sorted_df['Form'],
            sorted_df['Yield'] * 100
        ))
    ))
    
    fig.update_layout(
        title='Retail Price vs Actual Edible Cost (Top 15 Most Affordable)',
        xaxis_title='Fruit/Vegetable',
        yaxis_title='Price ($)',
        barmode='group',
        plot_bgcolor=colors['card_bg'],
        paper_bgcolor=colors['background'],
        font=dict(color=colors['text_primary']),
        xaxis=dict(tickangle=45),
        hovermode='x unified'
    )
    
    return fig

# Create summary statistics
summary_stats = {
    'total_items': len(df),
    'unique_items': df['Fruit'].nunique(),
    'avg_yield': df['Yield'].mean() * 100,
    'avg_actual_cost': avg_cost,
    'median_actual_cost': median_cost,
    'actual_cost_range': f"${df['ActualCostPerCup'].min():.2f} - ${df['ActualCostPerCup'].max():.2f}",
    'most_efficient': df.loc[df['Yield'].idxmax(), 'Fruit'],
    'highest_yield': df['Yield'].max() * 100,
    'lowest_cost_item': df.loc[df['ActualCostPerCup'].idxmin(), 'Fruit'],
    'lowest_cost': df['ActualCostPerCup'].min()
}