
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
    best_value_per_base_fruit, load_data, cheapest_items,
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
    return CSV_PATH   # default from utils.py: remote USDA GitHub URL


def _validate_csv(path: str) -> None:
    """Exit with a helpful message if a local path doesn't exist."""
    is_url = path.startswith("http://") or path.startswith("https://")
    if not is_url and not os.path.exists(path):
        sys.exit(
            f"\n[ERROR] CSV not found: {path}\n"
            f"  • Place your fruits.csv in a 'data/' folder next to run.py, OR\n"
            f"  • Run:  python run.py --csv /full/path/to/fruits.csv\n"
            f"  • OR set environment variable FRUITS_CSV=/path/to/fruits.csv\n"
        )


_csv_path = _resolve_csv()
_validate_csv(_csv_path)

# ── Load data ──────────────────────────────────────────────────────────────
df           = load_data(_csv_path)
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

def _hh_compute(strategy, cups):
    """Recompute household budget with a custom cups/day value."""
    import numpy as np
    import pandas as pd
    prices = df["CupEquivalentPrice"].sort_values().values
    n = len(prices)
    if strategy == "budget":
        ref = float(np.median(prices[: max(1, n // 4)]))
    elif strategy == "premium":
        ref = float(np.median(prices[3 * n // 4:]))
    else:
        ref = float(np.median(prices))
    rows = []
    for label, members in HOUSEHOLD_SIZES.items():
        annual = round(cups * ref * DAYS_PER_YEAR * members, 2)
        rows.append({
            "Household":    label,
            "Members":      members,
            "PricePerCup":  round(ref, 4),
            "Annual_Cost":  annual,
            "Monthly_Cost": round(annual / 12, 2),
            "Weekly_Cost":  round(annual / 52, 2),
            "Daily_Cost":   round(annual / DAYS_PER_YEAR, 2),
        })
    return pd.DataFrame(rows)


def fig_household(strategy, dark, cups=1.5, sel_hh=None, sel_cols=None):
    t = tok(dark)
    hh = _hh_compute(strategy, cups)
    if sel_hh:
        hh = hh[hh["Household"].isin(sel_hh)]
    if not sel_cols:
        sel_cols = ["Annual","Monthly","Weekly"]

    col_map = {
        "Annual":  ("Annual_Cost",  t["primary"]),
        "Monthly": ("Monthly_Cost", "#48aa68" if not dark else "#2ed581"),
        "Weekly":  ("Weekly_Cost",  t["accent"]),
        "Daily":   ("Daily_Cost",   "#60a5fa" if dark else "#3b82f6"),
    }
    fig = go.Figure()
    for label in sel_cols:
        col, color = col_map[label]
        fig.add_trace(go.Bar(
            name=label, x=hh["Household"], y=hh[col],
            marker_color=color, marker_line_width=0,
            hovertemplate=f"<b>%{{x}}</b><br>{label}: <b>$%{{y:,.2f}}</b><extra></extra>",
        ))
    title_map = {"budget":"Budget Mix (Cheapest 25%)",
                 "average":"Average Mix (Median)",
                 "premium":"Premium Mix (Costliest 25%)"}
    fig.update_layout(
        **base_lo(t, f"Household Fruit Cost — {title_map.get(strategy,'Average')} · {cups} cups/day"),
        barmode="group",
    )
    fig.update_yaxes(gridcolor=t["grid"], tickprefix="$", color=t["sub"])
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

def hh_rows(strategy, dark, cups=1.5, sel_hh=None, sel_cols=None):
    t   = tok(dark)
    hh  = _hh_compute(strategy, cups)
    if sel_hh:
        hh = hh[hh["Household"].isin(sel_hh)]
    if not sel_cols:
        sel_cols = ["Daily","Weekly","Monthly","Annual"]
    col_map = {
        "Daily":   ("Daily_Cost",   None),
        "Weekly":  ("Weekly_Cost",  None),
        "Monthly": ("Monthly_Cost", None),
        "Annual":  ("Annual_Cost",  t["primary"]),
    }
    cells_per_row = lambda r: (
        [_td(r["Household"], t, bold=True)] +
        [_td(f"${r[col_map[c][0]]:,.2f}", t, mono=True,
             bold=(c == "Annual"), color=(t["primary"] if c == "Annual" else None))
         for c in sel_cols]
    )
    return [dmc.TableTr(cells_per_row(r)) for _, r in hh.iterrows()]

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
        dcc.Store(id="hh-households-store", data=list(HOUSEHOLD_SIZES.keys())),
        dcc.Store(id="hh-cols-store",       data=["Annual","Monthly","Weekly","Daily"]),
        dcc.Store(id="hh-cups-store",       data=1.5),

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
                                dmc.TabsTab("Data Source", value="sources",
                                            leftSection=DashIconify(icon="mdi:database-outline",width=15)),
                            ]),
                        ]),
                    ])]),

            # CONTENT
            dmc.Container(size="xl",p="xl",children=[html.Div(id="tab-content")]),

            # FOOTER
            dmc.Box(id="ftr",
                    style={"borderTop":f"1px solid {LIGHT['border']}","padding":"18px 0","marginTop":"16px"},
                    children=[dmc.Container(size="xl",children=[
                        dmc.Group(justify="center",gap="xs",children=[
                            DashIconify(icon="mdi:database-outline",width=14,
                                        style={"color":"#888","marginTop":"2px"}),
                            dmc.Text("Data: ",size="xs",c="dimmed"),
                            dmc.Anchor(
                                "USDA ERS Fruit & Vegetable Prices",
                                href="https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices/",
                                target="_blank",
                                size="xs",
                                style={"color":"#2d8b6e","textDecoration":"underline"},
                            ),
                            dmc.Text(" (Updated Dec 2025)  •  1.5 cups/day per USDA Dietary Guidelines 2020–2025  •  Annual = daily cups × $/cup × 365",
                                     size="xs",c="dimmed"),
                        ]),
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
    Input("hh-households-store","data"),
    Input("hh-cols-store","data"),
    Input("hh-cups-store","data"),
)
def render(tab, dark, strategy, sel_hh, sel_cols, cups):
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
        cups     = cups or 1.5
        sel_hh   = sel_hh or list(HOUSEHOLD_SIZES.keys())
        sel_cols = sel_cols or ["Annual","Monthly","Weekly","Daily"]
        hh       = _hh_compute(strategy, cups)
        hh_disp  = hh[hh["Household"].isin(sel_hh)]

        content = dmc.Stack(gap="lg", children=[
            sec_hdr("Household Budget Projections",
                    "Filter by household type, time period, and daily intake to model your exact scenario.", t),

            # ── FILTER PANEL ─────────────────────────────────
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface"],"border":f"2px solid {t['primary']}"},
                      children=[
                dmc.Group(gap="xs", mb="sm", align="center", children=[
                    DashIconify(icon="mdi:filter-variant", width=18,
                                style={"color": t["primary"]}),
                    dmc.Text("Filters", fw=800, size="md", style={"color": t["primary"]}),
                    dmc.Badge("Interactive", color="green", variant="light", size="xs", radius="xl"),
                ]),
                dmc.SimpleGrid(cols={"base":1,"sm":2,"lg":4}, spacing="md", children=[

                    # 1. Shopping Strategy
                    dmc.Stack(gap=6, children=[
                        dmc.Text("Shopping Strategy", size="xs", fw=700, c="dimmed",
                                 style={"textTransform":"uppercase","letterSpacing":"0.06em"}),
                        dmc.SegmentedControl(
                            id="strategy-ctrl", value=strategy,
                            data=[{"label":"🛒 Budget","value":"budget"},
                                  {"label":"⚖️ Average","value":"average"},
                                  {"label":"🌟 Premium","value":"premium"}],
                            color="green", size="sm", fullWidth=True,
                        ),
                        dmc.Text(
                            f"Budget: ${_hh_compute('budget',cups)['PricePerCup'].iloc[0]:.4f}/cup  ·  "
                            f"Avg: ${_hh_compute('average',cups)['PricePerCup'].iloc[0]:.4f}/cup  ·  "
                            f"Premium: ${_hh_compute('premium',cups)['PricePerCup'].iloc[0]:.4f}/cup",
                            size="xs", c="dimmed",
                        ),
                    ]),

                    # 2. Daily Cups Intake
                    dmc.Stack(gap=6, children=[
                        dmc.Group(justify="space-between", children=[
                            dmc.Text("Daily Cups / Person", size="xs", fw=700, c="dimmed",
                                     style={"textTransform":"uppercase","letterSpacing":"0.06em"}),
                            dmc.Badge(f"{cups} cups/day", color="green", variant="light",
                                      size="sm", radius="xl"),
                        ]),
                        dmc.Slider(
                            id="cups-slider",
                            value=cups, min=1.0, max=3.0, step=0.5,
                            marks=[{"value":v,"label":f"{v}"} for v in [1.0,1.5,2.0,2.5,3.0]],
                            color="green", size="sm",
                        ),
                        dmc.Text(
                            "USDA recommends 1.5–2 cups/day for adults. "
                            "Children: 1–1.5 cups. Active adults: 2–2.5 cups.",
                            size="xs", c="dimmed",
                        ),
                    ]),

                    # 3. Household Types
                    dmc.Stack(gap=6, children=[
                        dmc.Text("Household Types", size="xs", fw=700, c="dimmed",
                                 style={"textTransform":"uppercase","letterSpacing":"0.06em"}),
                        dmc.MultiSelect(
                            id="hh-selector",
                            data=[{"label":k,"value":k} for k in HOUSEHOLD_SIZES.keys()],
                            value=sel_hh,
                            placeholder="Select households…",
                            clearable=True,
                            searchable=False,
                        ),
                        dmc.Text(f"{len(sel_hh)} of {len(HOUSEHOLD_SIZES)} household types shown.",
                                 size="xs", c="dimmed"),
                    ]),

                    # 4. Time Periods
                    dmc.Stack(gap=6, children=[
                        dmc.Text("Time Periods to Show", size="xs", fw=700, c="dimmed",
                                 style={"textTransform":"uppercase","letterSpacing":"0.06em"}),
                        dmc.MultiSelect(
                            id="cols-selector",
                            data=[{"label":c,"value":c} for c in ["Annual","Monthly","Weekly","Daily"]],
                            value=sel_cols,
                            placeholder="Select periods…",
                            clearable=True,
                            searchable=False,
                        ),
                        dmc.Text("Choose which time periods appear in the chart and table.",
                                 size="xs", c="dimmed"),
                    ]),
                ]),
            ]),

            # ── KPI MINI-CARDS ────────────────────────────────
            dmc.SimpleGrid(cols={"base":2,"sm":3,"lg":5}, spacing="sm", children=[
                dmc.Paper(
                    radius="md", p="md",
                    style={"background":t["surface2"],"border":f"1px solid {t['border']}",
                           "textAlign":"center",
                           "opacity":"1.0" if r["Household"] in sel_hh else "0.35"},
                    children=[
                        dmc.Text(r["Household"], size="xs", fw=700, c="dimmed"),
                        dmc.Text(f"${r['Annual_Cost']:,.0f}", size="xl", fw=900,
                                 style={"color": t["primary"] if r["Household"] in sel_hh else t["sub"],
                                        "fontVariantNumeric":"tabular-nums"}),
                        dmc.Text("per year", size="xs", c="dimmed"),
                        dmc.Text(f"${r['Monthly_Cost']:.2f}/mo", size="sm", fw=600,
                                 style={"color": t["accent"]}),
                        dmc.Text(f"${r['Daily_Cost']:.2f}/day", size="xs", c="dimmed"),
                    ],
                )
                for _, r in hh.iterrows()
            ]),

            # ── CHART ─────────────────────────────────────────
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                          dcc.Graph(
                              figure=fig_household(strategy, dark, cups, sel_hh, sel_cols),
                              config=PLOT_CONFIG,
                          ),
                      ]),

            # ── TABLE ─────────────────────────────────────────
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                dmc.Group(justify="space-between", align="center", mb="sm", children=[
                    dmc.Text("Breakdown Table", fw=700, style={"color":t["text"]}),
                    dmc.Badge(
                        f"{cups} cups/day · {strategy.title()} mix",
                        color="green", variant="light", size="sm", radius="xl",
                    ),
                ]),
                dmc.Table(
                    striped=True, highlightOnHover=True,
                    children=[
                        dmc.TableThead(dmc.TableTr(
                            [_th("Household", t)] +
                            [_th(c, t) for c in sel_cols]
                        )),
                        dmc.TableTbody(
                            hh_rows(strategy, dark, cups, sel_hh, sel_cols)
                        ),
                    ],
                ),
            ]),

            # ── COST INSIGHT CARD ─────────────────────────────
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface2"],"border":f"1px solid {t['border']}"},
                      children=[
                dmc.Group(gap="sm", mb="xs", align="center", children=[
                    DashIconify(icon="mdi:lightbulb-on-outline", width=20,
                                style={"color": t["accent"]}),
                    dmc.Text("What does this mean?", fw=700, style={"color":t["text"]}),
                ]),
                dmc.SimpleGrid(cols={"base":1,"sm":3}, spacing="md", children=[
                    dmc.Stack(gap=2, children=[
                        dmc.Text("Per day (1 adult)", size="xs", c="dimmed", fw=600),
                        dmc.Text(
                            f"${_hh_compute(strategy,cups).loc[0,'Daily_Cost']:.2f}",
                            size="xl", fw=900, style={"color":t["primary"],
                                                       "fontVariantNumeric":"tabular-nums"},
                        ),
                        dmc.Text(f"at {cups} cups · {strategy} mix", size="xs", c="dimmed"),
                    ]),
                    dmc.Stack(gap=2, children=[
                        dmc.Text("Monthly (family of 4)", size="xs", c="dimmed", fw=600),
                        dmc.Text(
                            f"${_hh_compute(strategy,cups).loc[3,'Monthly_Cost']:,.2f}",
                            size="xl", fw=900, style={"color":t["accent"],
                                                       "fontVariantNumeric":"tabular-nums"},
                        ),
                        dmc.Text(f"at {cups} cups · {strategy} mix", size="xs", c="dimmed"),
                    ]),
                    dmc.Stack(gap=2, children=[
                        dmc.Text("Annual savings (Budget vs Premium)", size="xs", c="dimmed", fw=600),
                        dmc.Text(
                            f"${abs(_hh_compute('premium',cups).loc[3,'Annual_Cost'] - _hh_compute('budget',cups).loc[3,'Annual_Cost']):,.2f}",
                            size="xl", fw=900, style={"color":"#2d8b6e",
                                                       "fontVariantNumeric":"tabular-nums"},
                        ),
                        dmc.Text("family of 4 · choosing cheapest vs premium fruits", size="xs", c="dimmed"),
                    ]),
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

    # ── DATA SOURCE ───────────────────────────────────────────
    elif tab == "sources":
        content = dmc.Stack(gap="lg", children=[
            sec_hdr("Data Source & Methodology",
                    "Full provenance, methodology, and citation information for this analysis.", t),

            # Main source card
            dmc.Paper(radius="md", p="xl", shadow="sm",
                      style={"background":t["surface"],"border":f"2px solid {t['primary']}"},
                      children=[
                dmc.Group(gap="md", align="flex-start", children=[
                    dmc.ThemeIcon(
                        DashIconify(icon="mdi:government-building", width=28),
                        size=56, radius="md", variant="light", color="green",
                    ),
                    dmc.Stack(gap=6, style={"flex":1}, children=[
                        dmc.Text("USDA Economic Research Service (ERS)",
                                 fw=900, size="lg", style={"color":t["text"]}),
                        dmc.Text("Fruit and Vegetable Prices Dataset",
                                 fw=600, size="md", style={"color":t["primary"]}),
                        dmc.Group(gap="xs", children=[
                            dmc.Badge("Updated Dec 9, 2025", color="green", variant="filled", size="sm"),
                            dmc.Badge("2023 Retail Scanner Data", color="teal",  variant="light", size="sm"),
                            dmc.Badge("150+ Items", color="blue",  variant="light", size="sm"),
                        ]),
                        dmc.Text(
                            "USDA ERS estimated average prices for more than 150 commonly consumed "
                            "fresh and processed fruits and vegetables. Prices are reported per edible "
                            "cup equivalent — the unit of measurement used in Federal recommendations "
                            "for fruit and vegetable consumption.",
                            size="sm", c="dimmed", mt=4,
                        ),
                        dmc.Anchor(
                            dmc.Group(gap=4, align="center", children=[
                                DashIconify(icon="mdi:open-in-new", width=14),
                                dmc.Text("www.ers.usda.gov/data-products/fruit-and-vegetable-prices",
                                         size="sm"),
                            ]),
                            href="https://www.ers.usda.gov/data-products/fruit-and-vegetable-prices/",
                            target="_blank",
                            style={"color": t["primary"]},
                        ),
                    ]),
                ]),
            ]),

            # Methodology grid
            dmc.SimpleGrid(cols={"base":1,"md":2}, spacing="md", children=[

                dmc.Paper(radius="md", p="lg", shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[
                    dmc.Group(gap="sm", mb="md", align="center", children=[
                        dmc.ThemeIcon(DashIconify(icon="mdi:calculator-variant",width=18),
                                      size="md",radius="xl",variant="light",color="green"),
                        dmc.Text("Price Calculation Methodology", fw=700, style={"color":t["text"]}),
                    ]),
                    dmc.Stack(gap="sm", children=[
                        dmc.Paper(p="sm", radius="sm",
                                  style={"background":t["surface2"],"border":f"1px solid {t['border']}"},
                                  children=[
                            dmc.Text("Weight-based items (per pound)", fw=600, size="sm",
                                     style={"color":t["primary"]}),
                            dmc.Code(
                                "CupPrice = (RetailPrice × CupSize) / Yield",
                                style={"fontSize":"0.8rem","display":"block","marginTop":"4px"},
                            ),
                        ]),
                        dmc.Paper(p="sm", radius="sm",
                                  style={"background":t["surface2"],"border":f"1px solid {t['border']}"},
                                  children=[
                            dmc.Text("Volume-based items / juices (per pint)", fw=600, size="sm",
                                     style={"color":t["primary"]}),
                            dmc.Code(
                                "CupPrice = RetailPrice × (CupSize / 16) / Yield",
                                style={"fontSize":"0.8rem","display":"block","marginTop":"4px"},
                            ),
                            dmc.Text("1 pint = 16 fl oz; cup-equiv = 8 fl oz",
                                     size="xs", c="dimmed", mt=4),
                        ]),
                        dmc.Paper(p="sm", radius="sm",
                                  style={"background":t["surface2"],"border":f"1px solid {t['border']}"},
                                  children=[
                            dmc.Text("Annual household cost", fw=600, size="sm",
                                     style={"color":t["primary"]}),
                            dmc.Code(
                                "Annual = CupPrice × cups/day × 365 × members",
                                style={"fontSize":"0.8rem","display":"block","marginTop":"4px"},
                            ),
                        ]),
                    ]),
                ]),

                dmc.Paper(radius="md", p="lg", shadow="sm",
                          style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                          children=[
                    dmc.Group(gap="sm", mb="md", align="center", children=[
                        dmc.ThemeIcon(DashIconify(icon="mdi:database-settings",width=18),
                                      size="md",radius="xl",variant="light",color="teal"),
                        dmc.Text("Data Collection", fw=700, style={"color":t["text"]}),
                    ]),
                    dmc.Stack(gap="sm", children=[
                        dmc.Group(align="flex-start", gap="sm", children=[
                            DashIconify(icon="mdi:check-circle",width=16,
                                        style={"color":t["primary"],"marginTop":"2px"}),
                            dmc.Text("Retail scanner data from Circana (2013, 2016, 2020, 2022, 2023)",
                                     size="sm", c="dimmed"),
                        ]),
                        dmc.Group(align="flex-start", gap="sm", children=[
                            DashIconify(icon="mdi:check-circle",width=16,
                                        style={"color":t["primary"],"marginTop":"2px"}),
                            dmc.Text("Stores include: grocery, supermarkets, supercenters, "
                                     "convenience, drug, and liquor stores nationwide.",
                                     size="sm", c="dimmed"),
                        ]),
                        dmc.Group(align="flex-start", gap="sm", children=[
                            DashIconify(icon="mdi:check-circle",width=16,
                                        style={"color":t["primary"],"marginTop":"2px"}),
                            dmc.Text("Prices are NOT suitable for year-to-year comparisons "
                                     "due to coding changes and market evolution.",
                                     size="sm", c="dimmed"),
                        ]),
                        dmc.Group(align="flex-start", gap="sm", children=[
                            DashIconify(icon="mdi:check-circle",width=16,
                                        style={"color":t["primary"],"marginTop":"2px"}),
                            dmc.Text("Updated annually, subject to data availability.",
                                     size="sm", c="dimmed"),
                        ]),
                        dmc.Divider(style={"borderColor":t["border"]}, mt="xs"),
                        dmc.Text("⚠ Disclaimer: Findings should not be attributed to Circana.",
                                 size="xs", c="dimmed", fs="italic"),
                    ]),
                ]),
            ]),

            # Dietary Guidelines reference + related publications
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                dmc.Group(gap="sm", mb="md", align="center", children=[
                    dmc.ThemeIcon(DashIconify(icon="mdi:book-open-variant",width=18),
                                  size="md",radius="xl",variant="light",color="orange"),
                    dmc.Text("Dietary Guidelines & Related Research", fw=700, style={"color":t["text"]}),
                ]),
                dmc.SimpleGrid(cols={"base":1,"md":2}, spacing="sm", children=[
                    *[
                        dmc.Paper(p="sm", radius="sm",
                                  style={"background":t["surface2"],"border":f"1px solid {t['border']}"},
                                  children=[
                            dmc.Group(gap="xs", align="flex-start", children=[
                                DashIconify(icon="mdi:file-document-outline",width=16,
                                            style={"color":t["primary"],"marginTop":"2px","flexShrink":"0"}),
                                dmc.Anchor(title, href=href, target="_blank", size="sm",
                                           style={"color":t["text"],"lineHeight":"1.4"}),
                            ]),
                        ])
                        for title, href in [
                            ("Satisfying Fruit & Vegetable Recommendations Possible for Under $3/Day (2024)",
                             "https://www.ers.usda.gov/amber-waves/2024/september/satisfying-fruit-and-vegetable-recommendations-possible-for-under-3-a-day-data-analysis-shows/"),
                            ("The Cost of Satisfying Fruit & Vegetable Recommendations in the Dietary Guidelines",
                             "https://www.ers.usda.gov/publications/pub-details/?pubid=42904"),
                            ("For SNAP Households, Fruit & Vegetable Affordability Is Partly a Question of Budgeting (2021)",
                             "https://www.ers.usda.gov/amber-waves/2021/july/for-supplemental-nutrition-assistance-program-snap-households-fruit-and-vegetable-affordability-is-partly-a-question-of-budgeting/"),
                            ("Americans Still Can Meet Fruit & Vegetable Guidelines for $2.10–$2.60/Day (2019)",
                             "https://www.ers.usda.gov/amber-waves/2019/june/americans-still-can-meet-fruit-and-vegetable-dietary-guidelines-for-2-10-2-60-per-day/"),
                            ("USDA Dietary Guidelines for Americans 2020–2025",
                             "https://www.dietaryguidelines.gov/resources/2020-2025-dietary-guidelines-online-materials"),
                            ("Download: All Fruits Average Prices (CSV)",
                             "https://www.ers.usda.gov/media/6210/all-fruits-average-prices-csv-format.csv"),
                        ]
                    ],
                ]),
            ]),

            # This dashboard's dataset summary
            dmc.Paper(radius="md", p="lg", shadow="sm",
                      style={"background":t["surface"],"border":f"1px solid {t['border']}"},
                      children=[
                dmc.Group(gap="sm", mb="md", align="center", children=[
                    dmc.ThemeIcon(DashIconify(icon="mdi:chart-timeline-variant",width=18),
                                  size="md",radius="xl",variant="light",color="violet"),
                    dmc.Text("This Dashboard's Dataset", fw=700, style={"color":t["text"]}),
                ]),
                dmc.SimpleGrid(cols={"base":2,"sm":3,"lg":6}, spacing="md", children=[
                    *[
                        dmc.Stack(gap=2, align="center",
                                  style={"textAlign":"center","padding":"12px",
                                         "background":t["surface2"],
                                         "borderRadius":"8px",
                                         "border":f"1px solid {t['border']}"},
                                  children=[
                            dmc.Text(val, fw=900, size="xl",
                                     style={"color":color,"fontVariantNumeric":"tabular-nums"}),
                            dmc.Text(label, size="xs", c="dimmed"),
                        ])
                        for val, label, color in [
                            (str(len(df)),              "Total Items",       t["primary"]),
                            (str(df["Form"].nunique()),  "Preparation Forms", t["accent"]),
                            (str(df["BaseFruit"].nunique()), "Base Fruits",  "#2d8b6e"),
                            (f"${stats['min']:.4f}",    "Lowest $/Cup",     "#48aa68"),
                            (f"${stats['max']:.4f}",    "Highest $/Cup",    "#e05252"),
                            (f"${stats['median']:.4f}", "Median $/Cup",     t["primary"]),
                        ]
                    ],
                ]),
            ]),
        ])

    else:
        content = dmc.Text("Select a tab", c="dimmed")

    return content, pw, hdr, nav, ftr


# ── Persist strategy from SegmentedControl ────────────────
@callback(
    Output("strategy-store","data"),
    Input("strategy-ctrl","value"),
    prevent_initial_call=True,
)
def save_strategy(v):
    return v

# ── Persist household selector ────────────────────────────
@callback(
    Output("hh-households-store","data"),
    Input("hh-selector","value"),
    prevent_initial_call=True,
)
def save_hh(v):
    return v or list(HOUSEHOLD_SIZES.keys())

# ── Persist column selector ───────────────────────────────
@callback(
    Output("hh-cols-store","data"),
    Input("cols-selector","value"),
    prevent_initial_call=True,
)
def save_cols(v):
    return v or ["Annual","Monthly","Weekly","Daily"]

# ── Persist cups slider ───────────────────────────────────
@callback(
    Output("hh-cups-store","data"),
    Input("cups-slider","value"),
    prevent_initial_call=True,
)
def save_cups(v):
    return v or 1.5


if __name__ == "__main__":
    app.run(debug=True, port=8050)