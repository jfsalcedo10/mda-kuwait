import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class SentimentCRUD(object):
    def __init__(self):
        self.base_df = pd.read_csv(
            './data/results_sa_all.txt', 
            infer_datetime_format=True, 
            parse_dates=["date"]
        )
    
    def plot_sentiment_over_time(self):
        df_sorted = self.base_df.sort_values('date')
        fig = go.Figure()

        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["stanza"], name = 'stanza', 
                                line=dict(color='#636EFA', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["textblob"], name = 'textblob', 
                                line=dict(color= '#EF553B', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["vader"], name = 'vader', 
                                line=dict(color='#00CC96', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["subjectivity"], name= 'subjectivity',
                                line=dict(color='#AB63FA', width=2)))

        fig.update_layout(title='Sentiment scores over time per method',
                        xaxis_title='Date',
                        yaxis_title='Score')
        
        return fig
