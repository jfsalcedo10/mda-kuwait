import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

class TopicCRUD(object):
    def __init__(self):
        self.base_df = pd.read_csv('./data/topic_plots_base.csv')
        # self.df_t = pd.read_csv('./data/topic_')
        self.df_p = pd.read_csv('./data/processed_speeches.txt')
        self.df_te = pd.read_csv("./data/token_embedding.txt").drop('Unnamed: 0', axis = 1)

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
    
    def get_top_tokens_per_topic(self, topic_ix = 4, nb_tokens = 10):
        # INPUT

        #################

        # NECESSARY DATA

        # df_t
        df_c = self.df_p.merge(self.base_df, on='title', validate="one_to_one")
        df_c = df_c[['title', 'fully_processed', 'main_topic_1_index']]

        #################
        topic_ix = topic_ix-1
        title = f'Topic {topic_ix+1}'

        # if plotted at the same time as the previous plot, this line can be left out (is already in previous cell)
        words = self.df_te.loc[topic_ix, :].sort_values(ascending=False).index.values[:nb_tokens] 

        # get the fully processed speeches for the given topic
        speeches = df_c.loc[df_c.main_topic_1_index==topic_ix,'fully_processed']
        # count the number of words in the topic
        nb_words_topic = speeches.str.split().str.len().sum()
        # count the number of words in all speeches
        nb_words_total = self.df_p.fully_processed.str.split().str.len().sum()

        count_for_topic = []
        total_count = []

        for w in words:
            # the count is only increased if the word is not part of another word (for example if w='gin', the count 
            # would not be increased if the word 'aging' is encountered)
            w = r'\b' + w.lower() + r'\b'
            # count the frequency of the word in the topic (as a percentage)
            count_for_topic.append(100*speeches.str.count(w).sum()/nb_words_topic)
            # count the frequency of the word in all speeches (as a percentage)
            total_count.append(100*df_c.fully_processed.str.count(w).sum()/nb_words_total)

        fig = go.Figure(data=[
            go.Bar(name='Total percentage', x=words, y=total_count, text=total_count, base=words,
                texttemplate = "%{text:.1f}%", marker=dict(color=px.colors.qualitative.Plotly[5])),
            go.Bar(name='Topic percentage', x=words, y=count_for_topic, text=count_for_topic, base=words,
                texttemplate = "%{text:.1f}%", marker=dict(color=px.colors.qualitative.Plotly[6]))
        ])

        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(title={'text':title, 'y':0.9, 'x':0.5, 'xanchor':'center', 'yanchor': 'top'},
                        barmode='group', uniformtext_minsize=12)
        return fig
    
    def get_token_influence(self, word = 'gun'):

        #################

        # NECESSARY DATA

        # df_t

        # df_p = pd.read_csv(csv_path / "processed_speeches.txt")
        df_c = self.df_p.merge(self.base_df, on='title', validate="one_to_one")
        df_c = df_c[['title', 'fully_processed', 'main_topic_1_index']]

        #################

        topics = list(range(0,25))
        title = f'Word: {word}'

        # the input has to be a word by itself, it cannot be part of another word. For example, 'gin' won't be counted when it
        # is part of another word like 'aging'
        word = r'\b' + word.lower() + r'\b'

        # total number of words in all speeches
        nb_words_total = self.df_p.fully_processed.str.split().str.len().sum()
        # frequency of the word in all speeches (as percentage)
        total_count = 100*df_c.fully_processed.str.count(word).sum()/nb_words_total

        count_for_topic = []
        for t in topics:
            # get the speeches for the topic
            speeches = df_c.loc[df_c.main_topic_1_index==t,'fully_processed']
            # number of words for the topic
            nb_words_topic = speeches.str.split().str.len().sum()
            # frequency of the word in the topic (as percentage)
            count_for_topic.append(100*speeches.str.count(word).sum()/nb_words_topic)

        topics = [str(int(t)+1) for t in topics]

        fig = go.Figure(data=[
            go.Bar(name='Topic percentage', x=topics, y=count_for_topic, text=count_for_topic,
                texttemplate = "%{text:.1f}%")
        ])

        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(title={'text':title, 'y':0.9, 'x':0.5, 'xanchor':'center', 'yanchor': 'top'},
                        barmode='group', uniformtext_minsize=15)


        fig.update_layout(xaxis = dict(title = 'Topic', tickmode = 'linear', tick0 = 1, dtick = 1 ),
            yaxis = dict(title= 'Percentage'))
        return fig

    def get_speech_topics(self):
        pass
