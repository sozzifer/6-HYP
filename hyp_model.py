import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stat

# Generate dataframes from csv
df_rda = pd.read_csv("data/rda.csv").reset_index(drop=True)
df_antacid = pd.read_csv("data/antacid.csv").reset_index(drop=True)
df_grades = pd.read_csv("data/grades.csv")

# Convert dataframes to lists
rda = df_rda["rda"].tolist()
antacid = df_antacid["antacid"].tolist()
grades = df_grades["grades"].tolist()

# Generate confidence interval from dataset, alternative hypothesis and confidence level (alpha) entered by the user - used to update graph
def update_statistics(dataset, alternative, alpha):
    fig = go.Figure()
    mean = np.mean(dataset)
    sem = stat.sem(dataset)
    nu = len(dataset) - 1
    if alternative == "<" or alternative == ">":
        conf_int = stat.t.interval(df=nu,
                                   confidence=alpha,
                                   loc=mean,
                                   scale=sem)
    else:
        conf_int = stat.t.interval(df=nu,
                                   confidence=(2*alpha)-1,
                                   loc=mean,
                                   scale=sem)
    return fig, conf_int

# 1-sided t-test - returns p value and confidence interval - used for Results section
def t_test_1sided(dataset, hyp_mean, alternative, alpha):
    mean = np.mean(dataset)
    sem = stat.sem(dataset)
    nu = len(dataset) - 1
    _, p = stat.ttest_1samp(a=dataset, popmean=hyp_mean, alternative=alternative)
    conf_int = stat.t.interval(df=nu,
                               confidence=alpha,
                               loc=mean,
                               scale=sem)
    if alternative == "less":
        conf_text = f"Upper bound for population mean: "
        conf_val = f"{conf_int[1]:.3f}"
    elif alternative == "greater":
        conf_text = "Lower bound for population mean: "
        conf_val = f"{conf_int[0]:.3f}"
    return p, conf_text, conf_val


# 2-sided t-test - returns p value and confidence interval - used for Results section
def t_test_2sided(dataset, hyp_mean, alpha):
    mean = np.mean(dataset)
    sem = stat.sem(dataset)
    nu = len(dataset) - 1
    _, p = stat.ttest_1samp(a=dataset, popmean=hyp_mean, alternative="two-sided")
    conf_int = stat.t.interval(df=nu,
                               confidence=(2*alpha)-1,
                               loc=mean,
                               scale=sem)
    conf_text = "Confidence interval for population mean: "
    conf_val = f"({conf_int[0]:.3f}, {conf_int[1]:.3f})"
    return p, conf_text, conf_val

# Create blank figure (UX)
def create_blank_fig():
    blank_fig = go.Figure(
        go.Histogram(x=antacid,
                     xbins={"start": 3, "end": 17, "size": 2},
                     name="Time to take<br>effect (mins)",
                     hovertemplate="Time (mins): %{x}" + "<br>Count: %{y}<extra></extra>",
                     marker_line_color="rgba(158,171,5,1)",
                     marker_color="rgba(158,171,5,0.5)",
                     marker_line_width=1,
                     showlegend=True),
            layout={"margin": dict(t=20, b=10, l=20, r=20),
                    "height": 400,
                    "font_size": 14})
    blank_fig.update_layout(dragmode=False)
    return blank_fig
