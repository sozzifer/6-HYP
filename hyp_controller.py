from dash import html, Input, Output, State, exceptions
import plotly.graph_objects as go
import numpy as np
import scipy.stats as stat
from hyp_model import antacid, grades, rda, alt_dict, add_ci_traces_lt, add_ci_traces_gt, add_ci_traces_eq
from hyp_view import app


@app.callback(
    Output("graph", "figure"),
    Output("sr-hist", "children"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alt-hyp-radio", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def update_histogram(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        fig = go.Figure(layout={"margin": dict(t=20, b=10, l=20, r=20),
                                "height": 400,
                                "font_size": 14})
        fig.update_layout(dragmode=False)
        if dataset == "antacid":
            fig.add_trace(go.Histogram(x=antacid,
                                       xbins={"start": 3, "end": 17, "size": 2},
                                       name="Time to take<br>effect (mins)",
                                       hovertemplate="Time (mins): %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[3, 17])
            sr_text = "Histogram of times for relief for new antacid tablet"
            mean = np.mean(antacid)
            sem = stat.sem(antacid)
            nu = len(antacid) - 1
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           confidence=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    add_ci_traces_lt(fig, 3, conf_int[1], hyp_mean)
                elif alternative == ">":
                    add_ci_traces_gt(fig, 17, conf_int[0], hyp_mean)
                return fig, sr_text
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                return fig, sr_text
        elif dataset == "grades":
            fig.add_trace(go.Histogram(x=grades,
                                       xbins={"start": 75, "end": 100, "size": 5},
                                       name="Grade",
                                       hovertemplate="Grade: %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[75, 100])
            sr_text = "Histogram of the grades of 30 students"
            mean = np.mean(grades)
            sem = stat.sem(grades)
            nu = len(grades) - 1
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           alpha=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    add_ci_traces_lt(fig, 75, conf_int[1], hyp_mean)
                elif alternative == ">":
                    add_ci_traces_gt(fig, 100, conf_int[0], hyp_mean)
                return fig, sr_text
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                return fig, sr_text
        elif dataset =="rda":
            fig.add_trace(go.Histogram(x=rda,
                                       xbins={"start": 5, "end": 21, "size": 2},
                                       name="Daily iron<br>intake (mg)",
                                       hovertemplate="RDA (mg): %{x}" + "<br>Count: %{y}<extra></extra>",
                                       marker_line_color="rgba(158,171,5,1)",
                                       marker_color="rgba(158,171,5,0.5)",
                                       marker_line_width=1))
            fig.update_xaxes(range=[5, 21])
            sr_text = "Histogram of iron intake for 45 randomly selected females aged under 51"
            mean = np.mean(rda)
            sem = stat.sem(rda)
            nu = len(rda) - 1
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           confidence=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    add_ci_traces_lt(fig, 5, conf_int[1], hyp_mean)
                elif alternative == ">":
                    add_ci_traces_gt(fig, 21, conf_int[0], hyp_mean)
                return fig, sr_text
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                add_ci_traces_eq(fig, conf_int[0], conf_int[1], hyp_mean)
                return fig, sr_text


@app.callback(
    Output("null-hyp", "children"),
    Output("alt-hyp", "children"),
    # Output("sample-mean", "children"),
    # Output("t-stat", "children"),
    Output("p-value", "children"),
    Output("p-store", "data"),
    Output("conf-text", "children"),
    Output("conf-val", "children"),
    Output("results", "style"),
    Output("accept-reject", "value"),
    Input("submit", "n_clicks"),
    State("dropdown", "value"),
    State("hyp-mean", "value"),
    State("alt-hyp-radio", "value"),
    State("alpha", "value"),
    prevent_initial_call=True
)
def perform_t_test(n_clicks, dataset, hyp_mean, alternative, alpha):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        alt = alt_dict[alternative]
        if dataset == "antacid":
            null_hyp = f"The actual mean time to relief for the new tablet is equal to the hypothesised mean ({hyp_mean} minutes)"
            mean = np.mean(antacid)
            sem = stat.sem(antacid)
            nu = len(antacid) - 1
            t, p = stat.ttest_1samp(a=antacid, popmean=hyp_mean, alternative=alt)
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           confidence=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    conf_text = f"Upper bound for population mean: "
                    conf_val = f"{conf_int[1]:.3f}"
                    alt_hyp = f"The actual mean time to relief for the new tablet is less than the hypothesised mean ({hyp_mean} minutes)"
                elif alternative == ">":
                    conf_text = "Lower bound for population mean: "
                    conf_val = f"{conf_int[0]:.3f}"
                    alt_hyp = f"The actual mean time to relief for the new tablet is greater than the hypothesised mean ({hyp_mean} minutes)"
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                conf_text = "Confidence interval for population mean: "
                conf_val = f"({conf_int[0]:.3f}, {conf_int[1]:.3f})"
                alt_hyp = f"The actual mean time to relief for the new tablet is NOT equal to the hypothesised mean ({hyp_mean} minutes)"
        elif dataset == "grades":
            null_hyp = f"The actual mean grade is equal to the hypothesised mean grade ({hyp_mean}%)"
            mean = np.mean(grades)
            sem = stat.sem(grades)
            nu = len(grades) - 1
            t, p = stat.ttest_1samp(
                a=grades, popmean=hyp_mean, alternative=alt)
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           confidence=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    conf_text = f"Upper bound for population mean: "
                    conf_val = f"{conf_int[1]:.3f}"
                    alt_hyp = f"The actual mean grade is less than the hypothesised mean grade ({hyp_mean}%)"
                elif alternative == ">":
                    conf_text = "Lower bound for population mean: "
                    conf_val = f"{conf_int[0]:.3f}"
                    alt_hyp = f"The actual mean grade is greater than the hypothesised mean grade ({hyp_mean}%)"
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                conf_text = "Confidence interval for population mean: "
                conf_val = f"({conf_int[0]:.3f}, {conf_int[1]:.3f})"
                alt_hyp = f"The actual mean grade is NOT equal to the hypothesised mean grade ({hyp_mean}%)"
        elif dataset == "rda":
            null_hyp = f"The actual mean intake of iron is equal to the hypothesised mean intake ({hyp_mean} milligrams)"
            mean = np.mean(rda)
            sem = stat.sem(rda)
            nu = len(rda) - 1
            t, p = stat.ttest_1samp(a=rda, popmean=hyp_mean, alternative=alt)
            if alternative == "<" or alternative == ">":
                conf_int = stat.t.interval(df=nu,
                                           confidence=alpha,
                                           loc=mean,
                                           scale=sem)
                if alternative == "<":
                    conf_text = f"Upper bound for population mean: "
                    conf_val = f"{conf_int[1]:.3f}"
                    alt_hyp = f"The actual mean intake of iron is less than the hypothesised mean intake ({hyp_mean} milligrams)"
                elif alternative == ">":
                    conf_text = "Lower bound for population mean: "
                    conf_val = f"{conf_int[0]:.3f}"
                    alt_hyp = f"The actual mean intake of iron is greater than the hypothesised mean intake ({hyp_mean} milligrams)"
            else:
                conf_int = stat.t.interval(df=nu,
                                           confidence=(2*alpha)-1,
                                           loc=mean,
                                           scale=sem)
                conf_text = "Confidence interval for population mean: "
                conf_val = f"({conf_int[0]:.3f}, {conf_int[1]:.3f})"
                alt_hyp = f"The actual mean intake of iron is NOT equal to the hypothesised mean intake ({hyp_mean} milligrams)"
        return null_hyp, alt_hyp, f"{p:.3f} ({p:.1%})", p,conf_text, conf_val, {"display": "inline"}, None
        # f"{mean:.2f}", f"{t:.3f}",

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
        marks = {75: {"label": "75%"},
                 80: {"label": "80%"},
                 85: {"label": "85%"},
                 90: {"label": "90%"},
                 95: {"label": "95%"},
                 100: {"label": "100%"}}
        text = "The grades of 30 students who took a test were recorded. The mean grade for previous tests was 80%. Is the mean grade for the observed 30 students the same or different to the mean for previous tests?"
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
    app.run(debug=False, host="0.0.0.0", port=8080, dev_tools_ui=False)
    # app.run(debug=True)
