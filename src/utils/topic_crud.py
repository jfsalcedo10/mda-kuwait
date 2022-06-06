import pandas as pd
import numpy as np
import plotly.express as px

class TopicCRUD(object):
    def __init__(self):
        self.base_df = pd.read_csv('./data/topic_plots_base.csv')

    def get_second_topic(self, topic_ix = 22):
        #################

        # NECESSARY DATA

        # df

        #################
        topic_ix = topic_ix-1
        title = f'Primary topic: topic {topic_ix+1}'

        # get all speeches where the main topic is the given one             
        m = self.base_df["main_topic_1_index"] == topic_ix

        # count the frequencies of the secondary topics
        topic_2 = pd.DataFrame(self.base_df.loc[m,:].main_topic_2_index.value_counts())
        # add a column with the topic number increased by one
        topic_2['topic'] = topic_2.index.values
        topic_2['topic'] = [str(int(t)+1) if t!='none' else 'none' for t in topic_2['topic']]

        # if 'none' is not in the list, order the data by descending frequency and ascending topic number
        # if 'none' is in the list, do the same and insert the row for 'none' as the last entry for its frequency
        if 'none' in topic_2['topic']:
            # select the rows where topic is a number so they can be sorted
            temp = topic_2.loc[topic_2.topic!='none', :].copy()
            temp['topic'] = temp['topic'].astype('int64')
            temp = temp.sort_values(by=['main_topic_2_index', 'topic'], ascending=[False, True])
            temp['topic'] = temp['topic'].astype('string')
            # insert the 'none' row
            none_count = topic_2.loc[topic_2.topic=='none', 'main_topic_2_index'].values[0]
            topic_2 = pd.concat(
                [
                    temp.loc[temp.main_topic_2_index>=none_count, :],
                    topic_2.loc[topic_2.topic=='none', :],
                    temp.loc[temp.main_topic_2_index<none_count, :]
                ], 
                ignore_index = True)
            
        else:
            # sort the values
            topic_2['topic'] = topic_2['topic'].astype('int64')
            topic_2 = topic_2.sort_values(by=['main_topic_2_index', 'topic'], ascending=[False, True])
            topic_2['topic'] = topic_2['topic'].astype('string')

        # plot
        fig = px.bar(topic_2, x="topic", y="main_topic_2_index", 
                    labels={"topic": "Secondary topic", "main_topic_2_index": "Count"})

        category_orders={"topic": topic_2['topic'].values}

        fig.update_layout(title={'text':title, 'y':0.95, 'x':0.5, 'xanchor':'center', 'yanchor': 'top'})

        return fig


    def get_topic_cities(self, topic_ix = 22, only_USA = False):

        # if False: color is based on country
        # if True: color is based on state (and non USA countries are not shown)
        # only_USA = False

        #################

        # NECESSARY DATA

        # df

        #################
        topic_ix = topic_ix-1
        title = f'Topic {topic_ix+1}'

        # get all speeches where the main topic is the given one             
        m = self.base_df["main_topic_1_index"] == topic_ix

        # count the frequencies of the cities
        cities = pd.DataFrame(self.base_df.loc[m,:].city.value_counts())
        cities['city_name'] = cities.index.values

        # add the country and state
        cities['country'] = cities.apply(lambda row: self.base_df.loc[self.base_df.city==row['city_name'], 'country'].values[0], axis=1)
        cities['state'] = cities.apply(lambda row: self.base_df.loc[self.base_df.city==row['city_name'], 'state'].values[0], axis=1)

        if only_USA:
            cities = cities.loc[cities.country=='USA', :]
            # color based on state
            color_var = 'state'
        else:
            # color based on country
            color_var = 'country'

        fig = px.bar(cities, x='city_name', y='city', color=color_var, 
                    hover_data= ['country', 'state', 'city_name', 'city'],
                    labels={'city_name': 'City','city': 'Count','country': 'Country','state': 'State'})

        fig.update_layout(title={'text':title, 'y':0.95, 'x':0.5, 'xanchor':'center', 'yanchor': 'top'})

        fig.update_traces(hovertemplate = '<b>Country</b>: %{customdata[0]}<br><b>State</b>: %{customdata[1]}'+
                        '<br><b>City</b>: %{x}<br><b>Count</b>: %{y}')  
        return fig
    
    def get_top_tokens_per_topic(self):
        pass
    
    def get_token_influence(self):
        pass

    def get_speech_topics(self):
        pass
