import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from pages.constants import TOPIC_COLORS

class SentimentCRUD(object):
    def __init__(self):
        self.base_df = pd.read_csv(
            './data/results_sa_all.txt', 
            infer_datetime_format=True, 
            parse_dates=["date"]
        )
        temp_df = pd.read_csv('./data/geo_df_sentiment.csv') 
        self.geo_df = gpd.GeoDataFrame(temp_df) #, crs='EPSG:4326')
        self.topic_colors = TOPIC_COLORS
    
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

    def plot_sentiment_location(self, location = True, stanza = True, color ='stanza'):
        fig = px.scatter_geo(self.geo_df, lat="latitude", lon="longitude",  color = color, #or color='stanza'
                      hover_name="title",
                     hover_data= {"latitude": False,
                                  "longitude": False,
                                  "location": location,
                                  "stanza": stanza},
                     projection="natural earth")

        fig.update_layout(
                title_text = 'Obama`s Speeches',
                showlegend = True,
                height=600
            
        # Layout of legend for the slides
        #         legend=dict(
        #             orientation="h",
        #             yanchor="bottom",
        #             y= -1,
        #             xanchor="right",
        #             x=1.3)
        )

        return fig

    def plot_sentiment_popularity_tracker(self):
        
        pass
