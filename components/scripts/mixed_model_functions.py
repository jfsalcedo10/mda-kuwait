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