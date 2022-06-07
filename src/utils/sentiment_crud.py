import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import geopandas as gpd
from pages.constants import TOPIC_COLORS


class SentimentCRUD(object):
    def __init__(self):
        self.base_df = pd.read_csv(
            './data/results_sa_all.txt',
            infer_datetime_format=True,
            parse_dates=["date"]
        ).sort_values("date")
        self.base_df = self.base_df[self.base_df["date"] >= "2009-01-27"]
        self.df_ppl = pd.read_csv(
            './data/obama-job-approval-ratings.txt',
            infer_datetime_format=True,
            parse_dates=["date"]
        ).sort_values("date")
        self.geo_df = gpd.GeoDataFrame(pd.read_csv(
            './data/geo_df_sentiment.csv')
        )
        
        self.gun_deaths_wide = pd.read_csv(
            './data/gun_deaths.csv'
        ).pivot(
            index="Year", columns="Intent", values = "Total"
        )
        self.gun_deaths_wide['Year2'] = self.gun_deaths_wide.index
        self.gun_deaths_wide = self.gun_deaths_wide.loc[(self.gun_deaths_wide['Year2'] > 2008) & (self.gun_deaths_wide['Year2'] < 2018)]
        self.gun_deaths_wide.rename(columns={"Total - all intents": "All_intents"}, inplace = True)
        
        self.topic_colors = TOPIC_COLORS

    def plot_sentiment_over_time(self):
        df_sorted = self.base_df.sort_values('date')
        fig = go.Figure()

        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["stanza"], name='stanza',
                                  line=dict(color='#636EFA', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["textblob"], name='textblob',
                                  line=dict(color='#EF553B', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["vader"], name='vader',
                                  line=dict(color='#00CC96', width=2)))
        fig.add_traces(go.Scatter(x=df_sorted["date"], y=df_sorted["subjectivity"], name='subjectivity',
                                  line=dict(color='#AB63FA', width=2)))

        fig.update_layout(title='Sentiment scores over time per method',
                          xaxis_title='Date',
                          yaxis_title='Score')

        return fig

    def plot_sentiment_location(self, location=True, stanza=True, color='stanza'):
        fig = px.scatter_geo(self.geo_df, lat="latitude", lon="longitude",  color=color,  # or color='stanza'
                             hover_name="title",
                             hover_data={"latitude": False,
                                         "longitude": False,
                                         "location": location,
                                         "stanza": stanza},
                             projection="natural earth")

        fig.update_layout(
            title_text='Obama`s Speeches',
            showlegend=True,
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
        # Plot sentiment plus ratings (together)

        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add popularity lines
        for col in self.df_ppl.columns[1:]:
            fig.add_trace(go.Scatter(x=self.df_ppl["date"],
                                     y=self.df_ppl[col], name=col),
                          secondary_y=True,)

        # Add sentiment lines
        for col in self.base_df.columns[2:]:
            if col == 'stanza' or col == 'textblob':
                fig.add_trace(go.Scatter(x=self.base_df["date"],
                                         y=self.base_df[col], name=col),
                              secondary_y=False,)

        # Add figure title
        fig.update_layout(  # height=600, width=1450,
            title={"text": "Job (Dis)Approval Distribition and Sentiment Scores over Time", "x": 0.3})

        # Set x-axis title
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Opinion ratio",
                         range=[0, 70], secondary_y=True)
        fig.update_yaxes(title_text="Sentiment score",
                         range=[-1.1, 1.1], secondary_y=False)

        return fig
    
    def plot_gun_popularity_tracker(self):
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Add sentiment lines
        for col in self.base_df.columns[2:]:
            if col == 'stanza' or  col == 'textblob' or col == 'weighted' :
                fig.add_trace(go.Scatter(x=self.base_df["date"],
                                y=self.base_df[col], name=col),
                                secondary_y=False,)
        # Add gun deaths lines
        for col in self.gun_deaths_wide.columns[0:6]:
            if col == 'Assault' or  col == 'Suicide' or col == 'All_intents' :
                fig.add_trace(go.Scatter(x=self.gun_deaths_wide["Year2"],
                            y=self.gun_deaths_wide[col], name=col),
                            secondary_y=True,)


        # Add figure title
        fig.update_layout(#height=600, width=1450,
            title = {"text":"Gun Deaths Frequencies and Sentiment Scores over Time", "x":0})

        # Set x-axis title
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Gun Deaths", range=[10000, 42000], secondary_y=True)
        fig.update_yaxes(title_text="Sentiment score",range=[-1.1,1.1], secondary_y=False)

        return fig
    
    # def plot_sentiment_time_neo4j(self):
    #     array=['Positive','Mixed','Neutral','Negative']
    #     # Create figure with secondary y-axis
    #     fig = make_subplots(specs=[[{"secondary_y": True}]])

    #     # Add traces
    #     fig.add_trace(
    #         go.Scatter(x=ndf_1["Date"], y=ndf_1["Sentiment"], name="Sentiment",line=dict(color='#636EFA', width=2)),
    #         secondary_y=False,
    #     )

    #     fig.add_trace(
    #         go.Scatter(x=ndf_1["Date"],y=ndf_1["Sentiment_score"], name="Confidence",line=dict(color='#00CC96', width=1)),
    #         secondary_y=True,
    #     )

    #     # Add figure title
    #     fig.update_layout(
    #         title_text="Sentiment over time"
    #     )

    #     # Set x-axis title
    #     fig.update_xaxes(title_text="Date")

    #     # Set y-axes titles and values
    #     fig.update_yaxes(title_text="<b>Primary axis</b> Sentiment", secondary_y=False,categoryorder='array', categoryarray= ['Negative','Neutral','Mixed','Positive'])
    #     fig.update_yaxes(title_text="<b>Secondary axis</b> Confidence", secondary_y=True,griddash="dot")

    #     return fig
