"""
run.py — U.S. Household Fruit Cost Dashboard
=============================================
Usage
-----
  python run.py                                  # uses data/fruits.csv (default)
  python run.py --csv /path/to/your/fruits.csv   # custom CSV location
"""
import argparse
import os
import sys

import dash_mantine_components as dmc
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from utils import (
    DAILY_CUPS_ADULT, DAYS_PER_YEAR, FORM_COLORS, HOUSEHOLD_SIZES,
    CSV_PATH,
    best_value_per_base_fruit, build_dataframe, cheapest_items,
    cost_summary_by_form, form_distribution, household_annual_budget,
    most_expensive_items, price_range_stats,
)

# ── Resolve CSV path (CLI arg → env var → utils default) ──────────────────
def _resolve_csv() -> str:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--csv", default=None)
    args, _ = parser.parse_known_args()
    if args.csv:
        return args.csv
    env = os.environ.get("FRUITS_CSV")
    if env:
        return env
    return CSV_PATH   # default from utils.py: <project>/data/fruits.csv

_csv_path = _resolve_csv()

if not os.path.exists(_csv_path):
    sys.exit(
        f"\n[ERROR] CSV not found: {_csv_path}\n"
        f"  • Place your fruits.csv in a 'data/' folder next to run.py, OR\n"
        f"  • Run:  python run.py --csv /full/path/to/fruits.csv\n"
        f"  • OR set environment variable FRUITS_CSV=/path/to/fruits.csv\n"
    )

# ── Load data ──────────────────────────────────────────────────────────────
df           = build_dataframe(_csv_path)
stats        = price_range_stats(df)
form_summary = cost_summary_by_form(df)
best_value   = best_value_per_base_fruit(df)
cheap_15     = cheapest_items(df, 15)
exp_15       = most_expensive_items(df, 15)
form_dist    = form_distribution(df)

LIGHT = {"bg":"#f3f8f5","surface":"#ffffff","surface2":"#eaf4ef","border":"#c8e0d4",
         "text":"#0f1e16","sub":"#4d7060","primary":"#1a7f5a","accent":"#f59e0b",
         "grid":"#ddeee5","header_grad":"linear-gradient(135deg,#0c3d27 0%,#1a7f5a 100%)"}
DARK  = {"bg":"#0e1b14","surface":"#152319","surface2":"#1d3026","border":"#2a4535",
         "text":"#e6f4ec","sub":"#7dab91","primary":"#2ed581","accent":"#fbbf24",
         "grid":"#1e3a2a","header_grad":"linear-gradient(135deg,#061108 0%,#0f3d24 100%)"}

FORM_COLORS_DARK = {"Fresh":"#2ed581","Canned":"#fb923c","Frozen":"#60a5fa",
                    "Dried":"#c084fc","Juice":"#fde047"}

PLOT_CONFIG = {"displayModeBar":True,
               "modeBarButtonsToRemove":["select2d","lasso2d","toImage"],
               "displaylogo":False}

def tok(dark): return DARK if dark else LIGHT
def fc(dark):  return FORM_COLORS_DARK if dark else FORM_COLORS

def base_lo(t, title="", height=None):
    lo = dict(paper_bgcolor=t["surface"], plot_bgcolor="rgba(0,0,0,0)",
              font=dict(family="'DM Sans',sans-serif", color=t["text"], size=12),
              margin=dict(l=10,r=10,t=44,b=10),
              title=dict(text=title, font=dict(size=14,color=t["text"]), x=0.01,xanchor="left"),
              legend=dict(bgcolor=t["surface2"],bordercolor=t["border"],borderwidth=1,
                          font=dict(size=11,color=t["text"])))
    if height: lo["height"]=height
    return lo

def fig_form_bars(dark):
    t=tok(dark)
    fig=go.Figure()
    for col,label,color in [("Annual_Min","Best-case","#48aa68"),
                              ("Annual_Avg","Typical",t["primary"]),
                              ("Annual_Max","Worst-case","#e05252")]:
        fig.add_trace(go.Bar(name=label, x=form_summary["Form"], y=form_summary[col],
                             marker_color=color, marker_line_width=0,
                             hovertemplate="<b>%{x}</b><br>"+label+": <b>$%{y:,.2f}</b>/yr<extra></extra>"))
    fig.update_layout(**base_lo(t,"Annual Per-Person Cost by Form"), barmode="group")
    fig.update_yaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_xaxes(color=t["sub"])
    return fig

def fig_strip(dark):
    t=tok(dark)
    fig=px.strip(df,x="Form",y="CupEquivalentPrice",color="Form",hover_name="Fruit",
                 color_discrete_map=fc(dark),
                 labels={"CupEquivalentPrice":"$/cup-equiv.","Form":""},
                 title="Price Distribution by Form")
    fig.update_traces(jitter=0.4,marker=dict(size=9,opacity=0.8,
                      line=dict(width=1,color=t["surface"])),
                      hovertemplate="<b>%{hovertext}</b><br>$%{y:.4f}/cup<extra></extra>")
    fig.update_layout(**base_lo(t,"Price Distribution by Form"))
    fig.update_yaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_xaxes(color=t["sub"])
    return fig

def fig_cheapest(dark):
    t=tok(dark)
    fig=px.bar(cheap_15,x="CupEquivalentPrice",y="Fruit",orientation="h",color="Form",
               color_discrete_map=fc(dark),text="CupEquivalentPrice",
               labels={"CupEquivalentPrice":"$/cup","Fruit":""},
               title="15 Most Affordable (per Cup-Equivalent)")
    fig.update_traces(texttemplate="$%{text:.3f}",textposition="outside",marker_line_width=0,
                      hovertemplate="<b>%{y}</b><br>$%{x:.4f}/cup<extra></extra>")
    fig.update_layout(**base_lo(t,"15 Most Affordable (per Cup-Equivalent)",height=490))
    fig.update_xaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_yaxes(color=t["sub"],categoryorder="total ascending")
    return fig

def fig_expensive(dark):
    t=tok(dark)
    fig=px.bar(exp_15,x="CupEquivalentPrice",y="Fruit",orientation="h",color="Form",
               color_discrete_map=fc(dark),text="CupEquivalentPrice",
               labels={"CupEquivalentPrice":"$/cup","Fruit":""},
               title="15 Most Expensive (per Cup-Equivalent)")
    fig.update_traces(texttemplate="$%{text:.3f}",textposition="outside",marker_line_width=0,
                      hovertemplate="<b>%{y}</b><br>$%{x:.4f}/cup<extra></extra>")
    fig.update_layout(**base_lo(t,"15 Most Expensive (per Cup-Equivalent)",height=490))
    fig.update_xaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_yaxes(color=t["sub"],categoryorder="total descending")
    return fig

def fig_household(strategy,dark):
    t=tok(dark)
    hh=household_annual_budget(df,strategy)
    fig=go.Figure()
    bars=[("Annual","Annual_Cost",t["primary"]),
          ("Monthly","Monthly_Cost","#48aa68" if not dark else "#2ed581"),
          ("Weekly","Weekly_Cost",t["accent"])]
    for label,col,color in bars:
        fig.add_trace(go.Bar(name=label,x=hh["Household"],y=hh[col],
                             marker_color=color,marker_line_width=0,
                             hovertemplate=f"<b>%{{x}}</b><br>{label}: <b>${{y:,.2f}}</b><extra></extra>"))
    title_map={"budget":"Budget Mix (Cheapest 25%)","average":"Average Mix (Median)",
               "premium":"Premium Mix (Costliest 25%)"}
    fig.update_layout(**base_lo(t,f"Household Fruit Cost — {title_map[strategy]}"),barmode="group")
    fig.update_yaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_xaxes(color=t["sub"])
    return fig

def fig_donut(dark):
    t=tok(dark)
    colors=[fc(dark).get(f,"#888") for f in form_dist["Form"]]
    fig=go.Figure(go.Pie(labels=form_dist["Form"],values=form_dist["Count"],hole=0.6,
                         marker=dict(colors=colors,line=dict(color=t["surface"],width=3)),
                         textinfo="label+percent",
                         hovertemplate="<b>%{label}</b><br>%{value} items (%{percent})<extra></extra>"))
    fig.update_layout(**base_lo(t,"Dataset Composition by Form"),showlegend=False)
    return fig

def fig_violin(dark):
    t=tok(dark)
    fig=go.Figure()
    for form in df["Form"].unique():
        sub=df[df["Form"]==form]
        fig.add_trace(go.Violin(x=[form]*len(sub),y=sub["Annual_Cost"],name=form,
                                fillcolor=fc(dark).get(form,"#888"),line_color=t["border"],
                                box_visible=True,meanline_visible=True,
                                hovertemplate="<b>%{x}</b><br>Annual: $%{y:,.2f}<extra></extra>"))
    fig.update_layout(**base_lo(t,"Annual Cost Distribution (1 Person) by Form"))
    fig.update_yaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_xaxes(color=t["sub"])
    return fig

def fig_scatter(dark):
    t=tok(dark)
    fig=px.scatter(df,x="RetailPrice",y="CupEquivalentPrice",color="Form",
                   size="Yield",hover_name="Fruit",color_discrete_map=fc(dark),
                   labels={"RetailPrice":"Retail Price ($/lb or $/pint)",
                           "CupEquivalentPrice":"Cup-Equivalent Price ($)","Yield":"Yield"},
                   title="Retail Price vs Cup-Equivalent Price")
    fig.update_traces(marker=dict(opacity=0.82,line=dict(width=1,color=t["surface"])),
                      hovertemplate="<b>%{hovertext}</b><br>Retail: $%{x:.4f}<br>Cup: $%{y:.4f}<extra></extra>")
    fig.update_layout(**base_lo(t,"Retail Price vs Cup-Equivalent Price"))
    fig.update_yaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    fig.update_xaxes(gridcolor=t["grid"],tickprefix="$",color=t["sub"])
    return fig

def fig_heatmap(dark):
    t=tok(dark)
    pivot=df.pivot_table(index="BaseFruit",columns="Form",values="CupEquivalentPrice",aggfunc="min")
    cs=[[0,"#084d36"],[0.5,"#48aa68"],[1,"#fef9c3"]] if not dark else \
       [[0,"#052810"],[0.5,"#1a7f5a"],[1,"#fefce8"]]
    fig=go.Figure(go.Heatmap(z=pivot.values,x=pivot.columns.tolist(),y=pivot.index.tolist(),
                              colorscale=cs,hoverongaps=False,
                              hovertemplate="<b>%{y}</b> — %{x}<br>$%{z:.4f}/cup<extra></extra>",
                              colorbar=dict(title="$/cup",tickprefix="$",
                                            tickfont=dict(color=t["sub"]),
                                            )))
    fig.update_layout(**base_lo(t,"Cup Price Heatmap: Fruit × Form",height=900))
    fig.update_yaxes(tickfont=dict(size=10),color=t["sub"])
    fig.update_xaxes(color=t["sub"])
    return fig

# ── UI HELPERS ──────────────────────────────────────────────
def kpi(label,value,sub,icon,color,dark):
    t=tok(dark)
    return dmc.Paper(radius="md",p="md",shadow="sm",
                     style={"background":t["surface"],"borderLeft":f"4px solid {color}",
                            "border":f"1px solid {t['border']}"},
                     children=[dmc.Group(justify="space-between",align="flex-start",children=[
                         dmc.Stack(gap=2,children=[
                             dmc.Text(label,size="xs",c="dimmed",fw=600,
                                      style={"textTransform":"uppercase","letterSpacing":"0.06em"}),
                             dmc.Text(value,size="xl",fw=900,
                                      style={"color":color,"fontVariantNumeric":"tabular-nums"}),
                             dmc.Text(sub,size="xs",c="dimmed"),
                         ]),
                         dmc.ThemeIcon(DashIconify(icon=icon,width=20),
                                       size="lg",radius="xl",variant="light",color="green"),
                     ])])

def sec_hdr(title,sub,t):
    return dmc.Stack(gap=2,mb="md",children=[
        dmc.Text(title,fw=800,size="lg",style={"color":t["text"]}),
        dmc.Text(sub,size="sm",c="dimmed"),
    ])

def _th(label,t):
    return dmc.TableTh(
        dmc.Text(label,fw=700,size="xs",
                 style={"textTransform":"uppercase","letterSpacing":"0.06em","color":t["sub"]}),
        style={"padding":"9px 12px","borderBottom":f"2px solid {t['primary']}",
               "background":t["surface2"]})

def _td(val,t,bold=False,mono=False,color=None):
    s={"padding":"7px 12px","borderBottom":f"1px solid {t['border']}"}
    if mono: s["fontFamily"]="monospace"
    if color: s["color"]=color
    if bold: s["fontWeight"]=700
    return dmc.TableTd(dmc.Text(val,size="sm",style=s))

def fbadge(form,dark):
    cm={"Fresh":"teal","Canned":"orange","Frozen":"blue","Dried":"violet","Juice":"yellow"}
    return dmc.Badge(form,color=cm.get(form,"gray"),
                     variant="light" if not dark else "filled",size="xs")

def hh_rows(strategy,dark):
    t=tok(dark)
    hh=household_annual_budget(df,strategy)
    return [dmc.TableTr([_td(r["Household"],t,bold=True),
                          _td(f"${r['Daily_Cost']:.2f}",t,mono=True),
                          _td(f"${r['Weekly_Cost']:.2f}",t,mono=True),
                          _td(f"${r['Monthly_Cost']:.2f}",t,mono=True),
                          _td(f"${r['Annual_Cost']:,.2f}",t,mono=True,bold=True,color=t["primary"])])
            for _,r in hh.iterrows()]

def full_table(dark):
    t=tok(dark)
    rows=[dmc.TableTr([
        _td(r["Fruit"],t,bold=True),
        dmc.TableTd(fbadge(r["Form"],dark),
                    style={"padding":"7px 12px","borderBottom":f"1px solid {t['border']}"}),
        _td(f"${r['RetailPrice']:.4f}",t,mono=True),
        _td(r["RetailPriceUnit"],t),
        _td(f"{r['Yield']:.2f}",t,mono=True),
        _td(f"${r['CupEquivalentPrice']:.4f}",t,mono=True,bold=True,color=t["primary"]),
        _td(f"${r['Annual_Cost']:,.2f}",t,mono=True,color=t["accent"]),
    ]) for _,r in df.sort_values("CupEquivalentPrice").iterrows()]
    return dmc.ScrollArea(h=480,children=dmc.Table(striped=True,highlightOnHover=True,
        style={"fontSize":"0.82rem"},children=[
            dmc.TableThead(dmc.TableTr([_th(h,t) for h in
                ["Fruit","Form","Retail Price","Unit","Yield","$/Cup","Annual/Person"]])),
            dmc.TableTbody(rows)]))

def bv_table(dark):
    t=tok(dark)
    bv=best_value.sort_values("CupEquivalentPrice")
    rows=[dmc.TableTr([
        _td(r["BaseFruit"],t,bold=True),
        dmc.TableTd(fbadge(r["Form"],dark),
                    style={"padding":"6px 10px","borderBottom":f"1px solid {t['border']}"}),
        _td(f"${r['CupEquivalentPrice']:.4f}",t,mono=True,bold=True,color=t["primary"]),
    ]) for _,r in bv.iterrows()]
    return dmc.ScrollArea(h=380,children=dmc.Table(striped=True,highlightOnHover=True,
        style={"fontSize":"0.82rem"},children=[
            dmc.TableThead(dmc.TableTr([_th(h,t) for h in ["Fruit","Best Form","$/Cup"]])),
            dmc.TableTbody(rows)]))

# ── APP ─────────────────────────────────────────────────────
app = Dash(__name__, title="FruitBudget Analytics",
           suppress_callback_exceptions=True,
           external_stylesheets=[
               "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&display=swap"])

app.layout = dmc.MantineProvider(
    id="mantine-provider",
    defaultColorScheme="light",
    theme={"primaryColor":"green","fontFamily":"'DM Sans',sans-serif","defaultRadius":"md"},
    children=[
        html.Link(rel="stylesheet",
                  href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800;900&display=swap"),
        dcc.Store(id="dark-store", data=False),
        dcc.Store(id="strategy-store", data="average"),

        dmc.Box(id="page-wrap", style={"background":LIGHT["bg"],"minHeight":"100vh"},children=[

            # HEADER
            dmc.Box(id="hdr",style={"background":LIGHT["header_grad"],"padding":"32px 0 24px"},children=[
                dmc.Container(size="xl",children=[
                    dmc.Group(justify="space-between",align="flex-start",children=[
                        dmc.Stack(gap=6,children=[
                            dmc.Group(gap="sm",align="center",children=[
                                DashIconify(icon="twemoji:green-apple",width=36),
                                dmc.Text("FruitBudget Analytics",
                                         style={"fontSize":"1.85rem","fontWeight":900,
                                                "color":"white","letterSpacing":"-0.02em"}),
                            ]),
                            dmc.Text("How much do U.S. households spend to meet fruit intake recommendations?",
                                     style={"color":"rgba(255,255,255,0.75)","maxWidth":620,"fontSize":"0.9rem"}),
                            dmc.Group(gap="xs",mt=4,children=[
                                dmc.Badge("USDA ERS Data",color="lime",variant="filled",radius="xl",size="sm"),
                                dmc.Badge(f"{len(df)} Fruit Items",color="teal",variant="light",radius="xl",size="sm"),
                                dmc.Badge("1.5 cups/day Recommended",color="green",variant="light",radius="xl",size="sm"),
                            ]),
                        ]),
                        dmc.Stack(gap=4,align="center",children=[
                            dmc.Tooltip(label="Toggle light / dark mode",children=
                                dmc.ActionIcon(DashIconify(icon="ph:moon-stars-bold",width=20,id="theme-icon"),
                                               id="theme-btn",variant="light",color="green",size="lg",radius="xl")),
                            dmc.Text("Dark mode",size="xs",style={"color":"rgba(255,255,255,0.6)"}),
                        ]),
                    ]),
                ]),
            ]),

            # STICKY NAV
            dmc.Box(id="nav-box",
                    style={"background":LIGHT["surface"],
                           "borderBottom":f"1px solid {LIGHT['border']}",
                           "position":"sticky","top":0,"zIndex":100},
                    children=[dmc.Container(size="xl",children=[
                        dmc.Tabs(id="tabs",value="overview",children=[
                            dmc.TabsList([
                                dmc.TabsTab("Overview",   value="overview",
                                            leftSection=DashIconify(icon="mdi:chart-bar",width=15)),
                                dmc.TabsTab("By Form",    value="byform",
                                            leftSection=DashIconify(icon="mdi:shape-outline",width=15)),
                                dmc.TabsTab("Households", value="households",
                                            leftSection=DashIconify(icon="mdi:account-group",width=15)),
                                dmc.TabsTab("Explorer",   value="explorer",
                                            leftSection=DashIconify(icon="mdi:table-search",width=15)),
                                dmc.TabsTab("Heatmap",    value="heatmap",
                                            leftSection=DashIconify(icon="mdi:grid",width=15)),
                            ]),
                        ]),
                    ])]),

            # CONTENT
            dmc.Container(size="xl",p="xl",children=[html.Div(id="tab-content")]),

            # FOOTER
            dmc.Box(id="ftr",
                    style={"borderTop":f"1px solid {LIGHT['border']}","padding":"18px 0","marginTop":"16px"},
                    children=[dmc.Container(size="xl",children=[
                        dmc.Text("Source: USDA ERS Fruit & Vegetable Prices Dataset  •  "
                                 "Recommendation: 1.5 cups/day (USDA Dietary Guidelines 2020–2025)  •  "
                                 "Annual cost = daily cups × $/cup × 365",
                                 size="xs",c="dimmed",ta="center"),
                    ])]),
        ]),
    ],
)

# ── DARK MODE TOGGLE ────────────────────────────────────────
@callback(
    Output("dark-store",       "data"),
    Output("mantine-provider", "forceColorScheme"),
    Output("theme-icon",       "icon"),
    Input("theme-btn",         "n_clicks"),
    State("dark-store",        "data"),
    prevent_initial_call=True,
)
def toggle_dark(n,dark):
    nd = not dark
    return nd, ("dark" if nd else "light"), ("ph:sun-bold" if nd else "ph:moon-stars-bold")

# ── RENDER TABS ─────────────────────────────────────────────
@callback(
    Output("tab-content","children"),
    Output("page-wrap","style"),
    Output("hdr","style"),
    Output("nav-box","style"),
    Output("ftr","style"),
    Input("tabs","value"),
    Input("dark-store","data"),
    Input("strategy-store","data"),
)
def render(tab, dark, strategy):
    t = tok(dark)
    pw  = {"background":t["bg"],"minHeight":"100vh","transition":"background 0.3s"}
    hdr = {"background":t["header_grad"],"padding":"32px 0 24px"}
    nav = {"background":t["surface"],"borderBottom":f"1px solid {t['border']}",
           "position":"sticky","top":0,"zIndex":100}
    ftr = {"borderTop":f"1px solid {t['border']}","padding":"18px 0","marginTop":"16px"}

    hh_avg = household_annual_budget(df,"average")
    s1  = hh_avg.loc[hh_avg["Members"]==1,"Annual_Cost"].values[0]
    s4  = hh_avg.loc[hh_avg["Members"]==4,"Annual_Cost"].values[0]

    # ── OVERVIEW ─────────────────────────────────────────────
    if tab == "overview":
        content = dmc.Stack(gap="lg",children=[
            dmc.SimpleGrid(cols={"base":1,"sm":2,"lg":4},spacing="md",children=[
                kpi("Median $/Cup-Equiv.",f"${stats['median']:.4f}",
                    "Across all 62 items","mdi:fruit-watermelon",t["primary"],dark),
                kpi("Cheapest Item",f"${stats['min']:.4f}",
                    "Watermelon (fresh)","mdi:arrow-down-circle","#2d8b6e",dark),
                kpi("Single Adult / Year",f"${s1:,.2f}",
                    "Median mix · 1.5 cups/day","mdi:account",t["accent"],dark),
                kpi("Family of 4 / Year",f"${s4:,.2f}",
                    "Median mix · 1.5 cups/day","mdi:account-group","#e07b39",dark),
            ]),
            dmc.Alert(
                dmc.Stack(gap=2,children=[
                    dmc.Text("Key Insight",fw=700,size="sm"),
                    dmc.Text(
                        f"At the median price of ${stats['median']:.4f}/cup-equivalent, "
                        f"a single adult needs only ${s1/365:.2f}/day to meet the USDA recommended "
                        f"1.5 cups of fruit. A family of four spends ~${s4/12:.2f}/month. "
                        f"Juice forms offer the lowest average annual cost "
                        f"(${form_summary.loc[form_summary['Form']=='Juice','Annual_Avg'].values[0]:,.2f}/yr), "
                        f"while canned items show the widest price range.",size="sm")]),
                color="green",variant="light" if not dark else "filled",
                icon=DashIconify(icon="mdi:lightbulb-on",width=20)),
            dmc.SimpleGrid(cols={"base":1,"lg":2},spacing="md",children=[
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_form_bars(dark),config=PLOT_CONFIG)]),
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_strip(dark),config=PLOT_CONFIG)]),
            ]),
            dmc.SimpleGrid(cols={"base":1,"lg":2},spacing="md",children=[
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_cheapest(dark),config=PLOT_CONFIG)]),
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_expensive(dark),config=PLOT_CONFIG)]),
            ]),
        ])

    # ── BY FORM ───────────────────────────────────────────────
    elif tab == "byform":
        content = dmc.Stack(gap="lg",children=[
            sec_hdr("Price Analysis by Preparation Form",
                    "Compare how different preparation methods affect affordability.",t),
            dmc.SimpleGrid(cols={"base":1,"sm":2,"lg":5},spacing="sm",children=[
                dmc.Paper(radius="md",p="md",
                          style={"background":t["surface"],
                                 "borderTop":f"4px solid {FORM_COLORS.get(r['Form'],'#888')}",
                                 "border":f"1px solid {t['border']}"},
                          children=[dmc.Stack(gap=2,children=[
                              dmc.Text(r["Form"],fw=800,size="sm",style={"color":t["text"]}),
                              dmc.Text(f"${r['AvgCupPrice']:.4f}",fw=900,size="lg",
                                       style={"color":FORM_COLORS.get(r["Form"],"#888"),
                                              "fontVariantNumeric":"tabular-nums"}),
                              dmc.Text("avg $/cup",size="xs",c="dimmed"),
                              dmc.Divider(style={"borderColor":t["border"]}),
                              dmc.Group(justify="space-between",children=[
                                  dmc.Stack(gap=0,align="center",children=[
                                      dmc.Text(f"${r['Annual_Min']:,.0f}",size="xs",fw=700,c="teal"),
                                      dmc.Text("min/yr",size="xs",c="dimmed")]),
                                  dmc.Stack(gap=0,align="center",children=[
                                      dmc.Text(f"${r['Annual_Avg']:,.0f}",size="xs",fw=700,
                                               style={"color":t["primary"]}),
                                      dmc.Text("avg/yr",size="xs",c="dimmed")]),
                                  dmc.Stack(gap=0,align="center",children=[
                                      dmc.Text(f"${r['Annual_Max']:,.0f}",size="xs",fw=700,c="red"),
                                      dmc.Text("max/yr",size="xs",c="dimmed")]),
                              ]),
                              dmc.Text(f"{int(r['Count'])} items",size="xs",c="dimmed",mt=2),
                          ])])
                for _,r in form_summary.iterrows()
            ]),
            dmc.SimpleGrid(cols={"base":1,"lg":2},spacing="md",children=[
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_violin(dark),config=PLOT_CONFIG)]),
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[dcc.Graph(figure=fig_donut(dark),config=PLOT_CONFIG)]),
            ]),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[dcc.Graph(figure=fig_scatter(dark),config=PLOT_CONFIG)]),
        ])

    # ── HOUSEHOLDS ────────────────────────────────────────────
    elif tab == "households":
        hh=household_annual_budget(df,strategy)
        content = dmc.Stack(gap="lg",children=[
            sec_hdr("Household Budget Projections",
                    "Estimate annual fruit spending for different household sizes and shopping strategies.",t),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[dmc.Group(justify="space-between",align="center",wrap="wrap",children=[
                          dmc.Stack(gap=2,children=[
                              dmc.Text("Shopping Strategy",fw=700,size="md",style={"color":t["text"]}),
                              dmc.Text(
                                  f"Budget ≈ ${household_annual_budget(df,'budget')['PricePerCup'].iloc[0]:.4f}/cup  ·  "
                                  f"Average ≈ ${household_annual_budget(df,'average')['PricePerCup'].iloc[0]:.4f}/cup  ·  "
                                  f"Premium ≈ ${household_annual_budget(df,'premium')['PricePerCup'].iloc[0]:.4f}/cup",
                                  size="xs",c="dimmed"),
                          ]),
                          dmc.SegmentedControl(id="strategy-ctrl",value=strategy,
                              data=[{"label":"🛒 Budget","value":"budget"},
                                    {"label":"⚖️ Average","value":"average"},
                                    {"label":"🌟 Premium","value":"premium"}],
                              color="green",size="md"),
                      ])]),
            dmc.SimpleGrid(cols={"base":2,"sm":3,"lg":5},spacing="sm",children=[
                dmc.Paper(radius="md",p="md",
                          style={"background":t["surface2"],"border":f"1px solid {t['border']}",
                                 "textAlign":"center"},
                          children=[
                              dmc.Text(r["Household"],size="xs",fw=700,c="dimmed"),
                              dmc.Text(f"${r['Annual_Cost']:,.0f}",size="xl",fw=900,
                                       style={"color":t["primary"],"fontVariantNumeric":"tabular-nums"}),
                              dmc.Text("per year",size="xs",c="dimmed"),
                              dmc.Text(f"${r['Monthly_Cost']:.2f}/mo",size="sm",fw=600,
                                       style={"color":t["accent"]}),
                          ])
                for _,r in hh.iterrows()
            ]),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[dcc.Graph(figure=fig_household(strategy,dark),config=PLOT_CONFIG)]),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                          dmc.Text("Breakdown Table",fw=700,mb="sm",style={"color":t["text"]}),
                          dmc.Table(striped=True,highlightOnHover=True,children=[
                              dmc.TableThead(dmc.TableTr([
                                  _th("Household",t),_th("Daily",t),_th("Weekly",t),
                                  _th("Monthly",t),_th("Annual",t)])),
                              dmc.TableTbody(hh_rows(strategy,dark)),
                          ]),
                      ]),
        ])

    # ── EXPLORER ──────────────────────────────────────────────
    elif tab == "explorer":
        content = dmc.Stack(gap="lg",children=[
            sec_hdr("Full Data Explorer",
                    "Browse all 62 fruit items sorted by cost-effectiveness.",t),
            dmc.SimpleGrid(cols={"base":1,"lg":2},spacing="md",children=[
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[
                              dmc.Text("Best-Value Form per Fruit",fw=700,mb="xs",style={"color":t["text"]}),
                              dmc.Text("Cheapest cup-equivalent option for each base fruit.",
                                       size="sm",c="dimmed",mb="md"),
                              bv_table(dark),
                          ]),
                dmc.Paper(radius="md",p="lg",shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[
                              dmc.Text("Price Distribution Statistics",fw=700,mb="md",style={"color":t["text"]}),
                              dmc.Stack(gap="sm",children=[
                                  *[
                                      dmc.Stack(gap=2,children=[
                                          dmc.Group(justify="space-between",children=[
                                              dmc.Text(label,size="sm",c="dimmed"),
                                              dmc.Text(f"${val:.4f}",fw=700,
                                                       style={"fontFamily":"monospace","color":color}),
                                          ]),
                                          dmc.Progress(value=val/stats["max"]*100,
                                                       color=pcolor,size="xs"),
                                      ])
                                      for label,val,color,pcolor in [
                                          ("Minimum", stats["min"], "#2d8b6e","teal"),
                                          ("25th Percentile", stats["q25"], t["primary"],"green"),
                                          ("Median", stats["median"], t["primary"],"green"),
                                          ("Mean", stats["mean"], t["accent"],"yellow"),
                                          ("75th Percentile", stats["q75"], "#e07b39","orange"),
                                          ("Maximum", stats["max"], "#b91c1c","red"),
                                      ]
                                  ],
                                  dmc.Divider(style={"borderColor":t["border"]}),
                                  dmc.Group(justify="space-between",children=[
                                      dmc.Text("Std Deviation",size="sm",c="dimmed"),
                                      dmc.Text(f"${stats['std']:.4f}",fw=600,
                                               style={"fontFamily":"monospace"}),
                                  ]),
                              ]),
                          ]),
            ]),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                          dmc.Text("Complete Dataset",fw=700,mb="md",style={"color":t["text"]}),
                          full_table(dark),
                      ]),
        ])

    # ── HEATMAP ───────────────────────────────────────────────
    elif tab == "heatmap":
        content = dmc.Stack(gap="lg",children=[
            sec_hdr("Cup-Equivalent Price Heatmap",
                    "Every fruit × form combination at a glance. Missing cells = form not available.",t),
            dmc.Paper(radius="md",p="lg",shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[dcc.Graph(figure=fig_heatmap(dark),config=PLOT_CONFIG)]),
        ])
    else:
        content = dmc.Text("Select a tab",c="dimmed")

    return content, pw, hdr, nav, ftr

# Update strategy store from SegmentedControl on Households tab
@callback(
    Output("strategy-store","data"),
    Input("strategy-ctrl","value"),
    prevent_initial_call=True,
)
def save_strategy(v):
    return v

if __name__ == "__main__":
    app.run(debug=True, port=8050)