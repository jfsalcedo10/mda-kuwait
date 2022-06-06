import pandas as pd
import numpy as np
from statsmodels.regression.mixed_linear_model import MixedLM


def process_covariate_data(data, pos_rating, neg_rating):
    df = data.transpose()
    df = df.iloc[1:, :]
    df.columns = [pos_rating, neg_rating]
    df['ratio'] = df[neg_rating] / df[pos_rating]
    df['date'] = pd.to_datetime(df.index.values, infer_datetime_format=True)
    df.index = list(range(len(df)))
    return df


def fit_mixed_model_with_covariate(df_full, covariate_data, pos_rating, neg_rating, fit_rating, fully_process):
    if fully_process:  # given data has not been transposed yet
        df_covariate = process_covariate_data(covariate_data, pos_rating, neg_rating)
    else:  # given data is already processed dataframe
        df_covariate = covariate_data

    # there are speeches years before the first rating, these have to be filtered out, otherwise they will
    # all be assigned the first rating
    df_fit = df_full.loc[df_full.date >= df_covariate.date.min()]

    # get the rating for each speech
    speech_dates = pd.DataFrame(df_fit.date.values).drop_duplicates()
    cov_ref = pd.DataFrame(speech_dates.values, columns=['date'])
    cov_ref[pos_rating] = cov_ref['date'].apply(lambda date: get_rating(date, df_covariate, pos_rating))
    cov_ref[neg_rating] = cov_ref['date'].apply(lambda date: get_rating(date, df_covariate, neg_rating))
    cov_ref['ratio'] = cov_ref['date'].apply(lambda date: get_rating(date, df_covariate, 'ratio'))

    # add the approval data to the dataframe
    df_fit = df_fit.merge(cov_ref, on='date', how='left')

    # fit the model
    mdfs = []
    for rating in fit_rating:
        vc = {'id': '0 + C(id)'}
        form = "sentiment ~ " + rating
        md = MixedLM.from_formula(form, groups='topic', data=df_fit,
                                  vc_formula=vc, re_formula='1', use_sqrt=True)
        mdf = md.fit()
        mdfs.append(mdf)

    return mdfs


def get_rating(date, ratings, which):
    # if there is an exact match for the date, get the rating for that date
    if date in ratings['date'].values:
        r = ratings.loc[ratings['date'] == date, which].values[0]

    else:  # get the rating for the date closest to the given one
        closest_dict = {
            abs(date - d): d
            for d in ratings['date'].values}
        closest_date = closest_dict[min(closest_dict.keys())]
        r = ratings.loc[ratings['date'] == closest_date, which].values[0]

    return r


def get_results_speech(pred_speech, eb, df_o, df_s):
    # predicted sentiment
    df_pred_speech = pred_speech.loc[:, pred_speech.columns != 'title'].merge(df_o, on='id', how='left')
    df_fitted_speech = df_pred_speech[['topic', 'id', 'title', 'Pred']].drop_duplicates()

    # EB estimates
    df_eb_speech = eb.loc[(eb.id != '_') & (eb.topic != '_')].copy()
    df_eb_speech = df_eb_speech[['id', 'Estimate']]
    df_eb_speech['id'] = df_eb_speech['id'].astype('int64')

    df_fitted_speech = df_fitted_speech.merge(df_eb_speech, on='id', how='left', validate='many_to_one')

    # additional info
    df_fitted_speech = df_fitted_speech.merge(df_s[['title', 'date', 'country', 'state', 'city']], on='title',
                                              how='left')

    return df_fitted_speech


def get_results_topic(eb):
    df_fitted_topic = eb.loc[(eb.id == '_') & (eb.topic != '_')].copy()
    df_fitted_topic['topic'] = df_fitted_topic['topic'].astype('int64') + 1
    df_fitted_topic = df_fitted_topic[['topic', 'Estimate']]
    return df_fitted_topic


def all_eb_estimates(df_fitted_speech, df_fitted_topic):
    # EB estimates of the speeches
    eb_speech = df_fitted_speech[['topic', 'id', 'title', 'Estimate']].copy()
    eb_speech.columns = ['topic', 'id', 'title', 'Estimate_speech']
    eb_speech['topic'] = eb_speech['topic'] + 1

    # EB estimates of the topics
    eb_topic = df_fitted_topic[['topic', 'Estimate']]
    eb_topic.columns = ['topic', 'Estimate_topic']

    eb = eb_speech.merge(eb_topic, on='topic', how='left', validate='many_to_one')
    return eb