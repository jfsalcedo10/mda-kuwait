import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

class UtilsCRUD(object):
    def __init__(self):
        self.df_ppl = pd.read_csv('./data/obama-job-approval-ratings.txt')
    
    def get_topic_titles(self):
        pass

    def plot_popularity(self):
        fig = px.line(self.df_ppl, x="date", y=["Approve","Disapprove"], 
              color_discrete_sequence=["green", "red"])
        fig.update_layout(title = {"text":"Obama approval rating [both periods]", "x":0.5},
                        legend_title = "Approval opinion",
                        xaxis_title = "Year",
                        yaxis_title = "Opinion ratio",
                        yaxis_range=[0,70])
        return fig