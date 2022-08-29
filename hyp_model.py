import pandas as pd
import plotly.graph_objects as go
import numpy as np

df_rda = pd.read_csv("data/rda.csv").reset_index(drop=True)
df_antacid = pd.read_csv("data/antacid.csv").reset_index(drop=True)
df_grades = pd.read_csv("data/grades.csv")

rda = df_rda["rda"].tolist()
antacid = df_antacid["antacid"].tolist()
grades = df_grades["grades"].tolist()

alt_dict = {"<": "less", ">": "greater", "!=": "two-sided"}


def add_ci_traces_lt(fig, start, ci_upper, hyp_mean):
    fig.add_trace(go.Scatter(x=np.linspace(start, ci_upper, 100),
                             y=[0.5]*100,
                             name="Confidence<br>interval",
                             hoverinfo="skip",
                             marker_color="#d10373"))
    fig.add_trace(go.Scatter(x=[start],
                             y=[0.5],
                             hoverinfo="skip",
                             marker_symbol="arrow-left",
                             marker_color="#d10373",
                             marker_size=14,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[ci_upper],
                             y=[0.5],
                             mode="markers",
                             hoverinfo="skip",
                             marker_symbol="line-ns",
                             marker_line_width=2,
                             marker_line_color="#d10373",
                             marker_size=12,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[hyp_mean],
                             y=[0.5],
                             name="Hypothesised<br>mean",
                             mode="markers",
                             hovertemplate="Hypothesised mean: %{x}<extra></extra>",
                             marker_symbol="circle-x-open",
                             marker_color="#d10373",
                             marker_size=16))


def add_ci_traces_gt(fig, end, ci_lower, hyp_mean):
    fig.add_trace(go.Scatter(x=np.linspace(ci_lower, end, 100),
                             y=[0.5]*100,
                             name="Confidence<br>interval",
                             hoverinfo="skip",
                             marker_color="#d10373"))
    fig.add_trace(go.Scatter(x=[end],
                             y=[0.5],
                             hoverinfo="skip",
                             marker_symbol="arrow-right",
                             marker_color="#d10373",
                             marker_size=14,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[ci_lower],
                             y=[0.5],
                             mode="markers",
                             hoverinfo="skip",
                             marker_symbol="line-ns",
                             marker_line_width=2,
                             marker_line_color="#d10373",
                             marker_size=12,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[hyp_mean],
                             y=[0.5],
                             name="Hypothesised<br>mean",
                             mode="markers",
                             hovertemplate="Hypothesised mean: %{x}<extra></extra>",
                             marker_symbol="circle-x-open",
                             marker_color="#d10373",
                             marker_size=16))


def add_ci_traces_eq(fig, ci_lower, ci_upper, hyp_mean):
    fig.add_trace(go.Scatter(x=[ci_lower, ci_upper],
                             y=[0.5, 0.5],
                             hoverinfo="skip",
                             name="Confidence<br>interval",
                             mode="lines",
                             marker_color="#d10373"))
    fig.add_trace(go.Scatter(x=[ci_lower],
                             y=[0.5],
                             mode="markers",
                             hoverinfo="skip",
                             marker_symbol="line-ns",
                             marker_line_width=2,
                             marker_line_color="#d10373",
                             marker_size=12,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[ci_upper],
                             y=[0.5],
                             mode="markers",
                             hoverinfo="skip",
                             marker_symbol="line-ns",
                             marker_line_width=2,
                             marker_line_color="#d10373",
                             marker_size=12,
                             showlegend=False)),
    fig.add_trace(go.Scatter(x=[hyp_mean],
                             y=[0.5],
                             name="Hypothesised<br>mean",
                             mode="markers",
                             hovertemplate="Hypothesised mean: %{x}<extra></extra>",
                             marker_symbol="circle-x-open",
                             marker_color="#d10373",
                             marker_size=16))
