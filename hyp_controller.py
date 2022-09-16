from dash import html, Input, Output, State, exceptions
import plotly.graph_objects as go
import numpy as np
from hyp_model import antacid, grades, rda, update_statistics, t_test_1sided, t_test_2sided
from hyp_view import app


# Add confidence interval lines and hypothesised mean location to graph for hypothesised mean < population mean
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


# Add confidence interval lines and hypothesised mean location to graph for hypothesised mean > population mean
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


# Add confidence interval lines and hypothesised mean location to graph for hypothesised mean = population mean
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

# Callback function to update graph and screen reader text for selected dataset and user entry for hypothesised mean, alternative hypothesis and confidence level (alpha)
@app.callback(
    Output("graph", "figure"),
    Output("sr-hist", "children"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alt-hyp-dropdown", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def update_histogram(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if dataset == "antacid":
            # Bins and x-axis start/end, bin size
            start = 3
            end = 17
            size = 2
            fig, conf_int = update_statistics(antacid, alternative, alpha)
            fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                              height=400,
                              font_size=14,
                              dragmode=False)
            fig.add_trace(go.Histogram(x=antacid,
                                       xbins={"start": start, "end": end, "size": size},
                                       name="Time to take<br>effect (mins)",
                                       hovertemplate="Time (mins): %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[start, end])
            if alternative == "<":
                add_ci_traces_lt(fig, start, conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of times for relief for new antacid tablet with upper bound for population mean of {conf_int[1]:.3f} and hypothesised mean of {hyp_mean}"
            elif alternative == ">":
                add_ci_traces_gt(fig, end, conf_int[0], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of times for relief for new antacid tablet with lower bound for population mean of {conf_int[0]:.3f} and hypothesised mean of {hyp_mean}"
            else:
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of times for relief for new antacid tablet with confidence interval ({conf_int[0]:.3f}, {conf_int[1]:.3f}) and hypothesised mean of {hyp_mean}"
        elif dataset == "grades":
            # Bins and x-axis start/end, bin size
            start = 75
            end = 100
            size = 5
            fig, conf_int = update_statistics(grades, alternative, alpha)
            fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                              height=400,
                              font_size=14,
                              dragmode=False)
            fig.add_trace(go.Histogram(x=grades,
                                       xbins={"start": start, "end": end, "size": size},
                                       name="Grade",
                                       hovertemplate="Grade: %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[start, end])
            if alternative == "<":
                add_ci_traces_lt(fig, start, conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of the grades of 30 students with upper bound for population mean of {conf_int[1]:.3f} and hypothesised mean of {hyp_mean}"
            elif alternative == ">":
                add_ci_traces_gt(fig, end, conf_int[0], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of the grades of 30 students with lower bound for population mean of {conf_int[0]:.3f} and hypothesised mean of {hyp_mean}"
            else:
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of the grades of 30 students with confidence interval ({conf_int[0]:.3f}, {conf_int[1]:.3f}) and hypothesised mean of {hyp_mean}"
        elif dataset =="rda":
            # Bins and x-axis start/end, bin size
            start = 5
            end = 21
            size = 2
            fig, conf_int = update_statistics(rda, alternative, alpha)
            fig.update_layout(margin=dict(t=20, b=10, l=20, r=20),
                              height=400,
                              font_size=14,
                              dragmode=False)
            fig.add_trace(go.Histogram(x=rda,
                                       xbins={"start": start, "end": end, "size": size},
                                       name="Daily iron<br>intake (mg)",
                                       hovertemplate="RDA (mg): %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[start, end])
            if alternative == "<":
                add_ci_traces_lt(fig, start, conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of iron intake for 45 randomly selected females aged under 51 with upper bound for population mean of {conf_int[1]:.3f} and hypothesised mean of {hyp_mean}"
            elif alternative == ">":
                add_ci_traces_gt(fig, end, conf_int[0], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of iron intake for 45 randomly selected females aged under 51 with lower bound for population mean of {conf_int[0]:.3f} and hypothesised mean of {hyp_mean}"
            else:
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                # Screen reader text
                sr_text = f"Histogram of iron intake for 45 randomly selected females aged under 51 with confidence interval ({conf_int[0]:.3f}, {conf_int[1]:.3f}) and hypothesised mean of {hyp_mean}"
        return fig, sr_text

# Callback function to generate natural language versions of the null/alternative hypothesis for the selected data set and display the p-value and confidence interval results
@app.callback(
    Output("null-hyp", "children"),
    Output("alt-hyp", "children"),
    Output("p-value", "children"),
    Output("p-store", "data"),
    Output("conf-text", "children"),
    Output("conf-val", "children"),
    # Results hidden until callback triggered
    Output("results", "style"),
    # Hide Conclusion feedback whenever callback triggered
    Output("accept-reject", "value"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alt-hyp-dropdown", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def perform_t_test(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        if dataset == "antacid":
            null_hyp = f"The actual mean time to relief for the new tablet is {hyp_mean} minutes"
            if alternative == "<":
                p, conf_text, conf_val = t_test_1sided(antacid, hyp_mean, "less", alpha)
                alt_hyp = f"The actual mean time to relief for the new tablet is less than {hyp_mean} minutes"
            elif alternative == ">":
                p, conf_text, conf_val = t_test_1sided(antacid, hyp_mean, "greater", alpha)
                alt_hyp = f"The actual mean time to relief for the new tablet is greater than {hyp_mean} minutes"
            else:
                p, conf_text, conf_val = t_test_2sided(antacid, hyp_mean, alpha)
                alt_hyp = f"The actual mean time to relief for the new tablet is NOT equal to {hyp_mean} minutes"
        elif dataset == "grades":
            null_hyp = f"The actual mean grade is equal to {hyp_mean}"
            if alternative == "<":
                p, conf_text, conf_val = t_test_1sided(grades, hyp_mean, "less", alpha)
                alt_hyp = f"The actual mean grade is less than {hyp_mean}"
            elif alternative == ">":
                p, conf_text, conf_val = t_test_1sided(grades, hyp_mean, "greater", alpha)
                alt_hyp = f"The actual mean grade is greater than {hyp_mean}"
            else:
                p, conf_text, conf_val = t_test_2sided(grades, hyp_mean, alpha)
                alt_hyp = f"The actual mean grade is NOT equal to {hyp_mean}"
        elif dataset == "rda":
            null_hyp = f"The actual mean intake of iron is equal to {hyp_mean} milligrams"
            if alternative == "<":
                p, conf_text, conf_val = t_test_1sided(rda, hyp_mean, "less", alpha)
                alt_hyp = f"The actual mean intake of iron is less than {hyp_mean} milligrams"
            elif alternative == ">":
                p, conf_text, conf_val = t_test_1sided(rda, hyp_mean, "greater", alpha)
                alt_hyp = f"The actual mean intake of iron is greater than {hyp_mean} milligrams"
            else:
                p, conf_text, conf_val = t_test_2sided(rda, hyp_mean, alpha)
                alt_hyp = f"The actual mean intake of iron is NOT equal to {hyp_mean} milligrams"
        return null_hyp, alt_hyp, f"{p:.3f} ({p:.1%})", p, conf_text, conf_val, {"display": "inline"}, None


# Callback function to give feedback when user decides whether to accept/reject the null hypothesis based on the calculated p-value
@app.callback(
    Output("conclusion", "children"),
    Input("accept-reject", "value"),
    State("p-store", "data"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def accept_or_reject(accept_reject, p, alpha):
    if accept_reject is None:
        return ""
    else:
        if accept_reject == "reject":
            if p < 1 - alpha:
                conclusion = [html.Span("Correct", className="bold-p"), html.Span(children=[f" - {p:.3f} is less than {(1-alpha):.2f}, so we reject the null hypothesis at the {alpha:.0%} confidence level"])]
            else:
                conclusion = [html.Span("Incorrect", className="bold-p"), html.Span(children=[f" - {p:.3f} is greater than {(1-alpha):.2f}, so we accept the null hypothesis at the {alpha:.0%} confidence level"])]
        elif accept_reject == "accept":
            if p < 1 - alpha:
                conclusion = [html.Span("Incorrect", className="bold-p"), html.Span(children=[f" - {p:.3f} is less than {(1-alpha):.2f}, so we reject the null hypothesis at the {alpha:.0%} confidence level"])]
            else:
                conclusion = [html.Span("Correct", className="bold-p"), html.Span(children=[f" - {p:.3f} is greater than {(1-alpha):.2f}, so we accept the null hypothesis at the {alpha:.0%} confidence level"])]
        return conclusion


# Callback function to update hypothesised mean slider based on selected dataset, so that user entered values give sensible results. Also updates data description text
@app.callback(
    Output("hyp-mean", "min"),
    Output("hyp-mean", "max"),
    Output("hyp-mean", "value"),
    Output("hyp-mean", "marks"),
    Output("data-text", "children"),
    Input("dropdown", "value")
)
def update_data_info(dataset):
    if dataset == "grades":
        hyp_min = 75
        hyp_max = 100
        hyp_mean = 80
        marks = {75: {"label": "75"},
                 80: {"label": "80"},
                 85: {"label": "85"},
                 90: {"label": "90"},
                 95: {"label": "95"},
                 100: {"label": "100"}}
        text = "The grades of 30 students who took a test were recorded. The mean grade for previous tests was 80. Is the mean grade for the observed 30 students the same or different to the mean for previous tests?"
    elif dataset == "antacid":
        hyp_min = 3
        hyp_max = 17
        hyp_mean = 12
        marks = {3: {"label": "3"},
                 4: {"label": "4"},
                 5: {"label": "5"},
                 6: {"label": "6"},
                 7: {"label": "7"},
                 8: {"label": "8"},
                 9: {"label": "9"},
                 10: {"label": "10"},
                 11: {"label": "11"},
                 12: {"label": "12"},
                 13: {"label": "13"},
                 14: {"label": "14"},
                 15: {"label": "15"},
                 16: {"label": "16"},
                 17: {"label": "17"}}
        text = "A chemist working for a pharmaceutical company has developed a new antacid tablet that she feels will relieve pain more quickly than the company's present tablet. Experience indicates that the present tablet requires an average of 12 minutes to take effect. The chemist records 15 times to relief with the new tablet. Does the new tablet work more quickly than the present tablet?"
    elif dataset == "rda":
        hyp_min = 5
        hyp_max = 21
        hyp_mean = 18
        marks = {5: {"label": "5"},
                 6: {"label": "6"},
                 7: {"label": "7"},
                 8: {"label": "8"},
                 9: {"label": "9"},
                 10: {"label": "10"},
                 11: {"label": "11"},
                 12: {"label": "12"},
                 13: {"label": "13"},
                 14: {"label": "14"},
                 15: {"label": "15"},
                 16: {"label": "16"},
                 17: {"label": "17"},
                 18: {"label": "18"},
                 19: {"label": "19"},
                 20: {"label": "20"},
                 21: {"label": "21"}}
        text = "The Food and Nutrition Authority of the National Academy of Sciences states that the Recommended Daily Amount (RDA) of iron for adult females under the age of 51 should be 18 milligrams (mg). Iron intakes, in mg, were obtained for a randomly selected group of 45 adult females under the age of 51, during a 24-hour period. Do adult females get less than the RDA of 18mg of iron?"
    return hyp_min, hyp_max, hyp_mean, marks, text


if __name__ == "__main__":
    app.run(debug=True)
    # To deploy on Docker, replace app.run(debug=True) with the following:
    # app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
