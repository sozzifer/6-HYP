from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from hyp_model import antacid, create_blank_fig

app = Dash(__name__,
           title="One-sample Hypothesis Testing",
           update_title=None,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{"name": "viewport",
                       "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Div([
                dbc.Label("Data set",
                          className="label",
                          html_for="dropdown"),
                dbc.Select(id="dropdown",
                           options=[{"label": "Antacid", "value": "antacid"},
                                    {"label": "Grades", "value": "grades"},
                                    {"label": "RDA", "value": "rda"}],
                           value="antacid"),
                html.Br()
            ], **{"aria-live": "polite"}),
            dbc.Label("Data description", className="label"),
            html.P(id="data-text", **{"aria-live": "polite"})
        ], xs=12, xl=6),
        dbc.Col([
            html.Div([
                dbc.Label("Alternative hypothesis",
                          className="label",
                          html_for="alt-hyp-radio"),
                dbc.Select(id="alt-hyp-radio",
                           options=[
                               {"label": u"Population mean \u2260 hypothesised mean (two-sided)", "value": "!="},
                               {"label": "Population mean < hypothesised mean (one-sided)", "value": "<"},
                               {"label": "Population mean > hypothesised mean (one-sided)", "value": ">"}],
                           value="!=")
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Label("Hypothesised mean",
                          className="label",
                          html_for="hyp-mean"),
                dcc.Slider(id="hyp-mean",
                           value=12,
                           min=3,
                           max=17,
                           step=1)
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Label("Confidence level",
                          className="label",
                          html_for="alpha"),
                dcc.Slider(id="alpha",
                           value=0.95,
                           min=0.8,
                           max=0.99,
                           marks={0.8: {"label": "80%"},
                                  0.85: {"label": "85%"},
                                  0.9: {"label": "90%"},
                                  0.95: {"label": "95%"},
                                  0.99: {"label": "99%"}})
            ], **{"aria-live": "polite"}),
            html.Div([
                dbc.Button(id="submit",
                           n_clicks=0,
                           children="Update results",
                           class_name="button",
                           style={"width": 150})
            ], className="d-flex justify-content-center"),
        ], xs=12, xl=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div([
                dcc.Graph(id="graph",
                          figure=create_blank_fig(),
                          config={"displayModeBar": False,
                                  "doubleClick": False,
                                  "editable": False,
                                  "scrollZoom": False,
                                  "showAxisDragHandles": False})
            ], role="img", style={"margin": "10px"}),
            html.Div(id="sr-hist",
                     children=[],
                     className="sr-only",
                     **{"aria-live": "polite"}),
            html.Br()
        ], xs=12, lg=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Results", style={"text-align": "center"}),
                    html.Div([
                        html.P("Null hypothesis", className="bold-p"),
                        html.P(id="null-hyp"),
                        html.P("Alternative hypothesis", className="bold-p"),
                        html.P(id="alt-hyp"),
                        html.Br(),
                        # html.P(children=[
                        #     html.Span("Sample mean: ", className="bold-p"),
                        #     html.Span(id="sample-mean")
                        # ]),
                        # html.P(children=[
                        #     html.Span("Test statistic: ", className="bold-p"),
                        #     html.Span(id="t-stat")
                        # ]),
                        html.P(children=[
                            html.Span("P value: ", className="bold-p"),
                            html.Span(id="p-value"),
                            dcc.Store(id="p-store")
                        ]),
                        html.P(children=[
                            html.Span(id="conf-text", className="bold-p"),
                            html.Span(id="conf-val")
                        ]),
                        html.Br(),
                        html.P(
                            "Based on the results above, should you accept or reject the null hypothesis?", className="bold-p"),
                        dbc.Select(id="accept-reject",
                                   options=[
                                        {"label": "Accept the null hypothesis",
                                         "value": "accept"},
                                        {"label": "Reject the null hypothesis",
                                         "value": "reject"}],
                                   value=None),
                        html.Br(),
                        html.P(id="conclusion", children=[])
                    ], id="results", style={"display": "none"}, **{"aria-live": "polite"}),
                ])
            ])
        ], xs=12, lg=6)
    ])
], fluid=True)
