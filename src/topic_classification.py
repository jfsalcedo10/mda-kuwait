import pandas as pd

import nltk
from nltk.corpus import wordnet


# code adapted from https://github.com/despiegj/goz39a/blob/mda_2022/textmining/nltk/normalisation.ipynb
# function to convert nltk tag to wordnet tag
def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


# code adapted from https://github.com/despiegj/goz39a/blob/mda_2022/textmining/nltk/normalisation.ipynb
def lemmatize_sentence(sentence, tokenizer, lemmatizer):
    # tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(tokenizer.tokenize(sentence))
    # tuple of (word, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


def normalize_text(text, tokenizer, lemmatizer):
    normalized_text = ""
    for sentence in text:
        normalized_text += " " + lemmatize_sentence(sentence, tokenizer, lemmatizer)
    return normalized_text


def remove_stopwords(text, stop_words):
    return " ".join([word for word in str(text).split() if word not in stop_words])


def classify_topics(lda_model, tf_matrix, titles):
    classification = 100 * lda_model.transform(tf_matrix)  # converted to percentages
    cnames = ['Topic ' + str(i) for i in range(1, lda_model.n_components + 1)]
    classification_df = pd.DataFrame(classification, columns=cnames)
    classification_df["title"] = titles
    return classification_df


def nb_topics_above_percentage(classification_df, percentage):
    cname = "nb_topics_above_" + str(percentage) + "_percent"
    select = classification_df.columns.str.startswith("Topic ")
    classification_df.loc[:, cname] = classification_df.loc[:, select].gt(percentage).sum(axis=1)


def percentage_speeches_above_percentage(percentage, nb_speeches, classification_df, topics_df):
    cname = 'percentage_speeches_above_' + str(percentage) + '_percent'
    select = classification_df.columns.str.startswith("Topic ")
    topics_df[cname] = classification_df.loc[:, select].gt(percentage).sum(axis=0) * 100 / nb_speeches


def sum_of_n_largest(n, classification_df):
    cname = 'sum_of_' + str(n) + '_largest'
    select = classification_df.columns.str.startswith("Topic ")
    classification_df.loc[:, cname] = classification_df.loc[:, select].apply(
        lambda row: row.nlargest(n).sum(), axis=1)


def sort_topics_per_speech(n_comp, classification_df):
    for i in range(1, n_comp + 1):
        cname = 'main_topic_' + str(i)
        select = classification_df.columns.str.startswith("Topic ")
        classification_df.loc[:, cname] = classification_df.loc[:, select].apply(
            lambda row: row.nlargest(i).index.values[i - 1], axis=1)
        select = classification_df.columns.str.startswith("Topic ")
        classification_df.loc[:, cname + '_perc'] = classification_df.loc[:, select].apply(
            lambda row: row.nlargest(i).values[i - 1], axis=1)
