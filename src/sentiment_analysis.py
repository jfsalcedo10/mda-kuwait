# Libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from datetime import datetime
import os
import sys
import stanza
import pandas as pd

#----------------------------------------------------------------------------------------------------------------#
# Utils functions

# Function to clean an specific character (expand if you need to clean more)
def clean_txt(string):
    string = string.replace(" -- ", ", ")
    return string



#----------------------------------------------------------------------------------------------------------------#
# Functions to call the models

# Stanza
def stanza_fn (string, j, max_j):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if j == 0:
        print(f"Stanza starts working at {time}")
    print(f"\rStanza working in speech {j} at {time}", end="")         # This reprint the line in the same space

    nlp = stanza.Pipeline('en', processors='tokenize, mwt, pos, lemma, depparse,sentiment',
                               use_gpu=False, verbose=False, pos_batch_size=3000) 
    doc = nlp(string)
    doc_sent = []
    for i, sentence in enumerate(doc.sentences):        
        doc_sent.append(sentence.sentiment)
    result = (sum(doc_sent)/len(doc_sent)) - 1                         # Change the reference

    time = now.strftime("%H:%M:%S")
    if j == max_j:
        print(f"\nStanza finished working at {time}")

    return result                   # [0 negative, 1 neutral, 2 positive] Now -1 negative, 0 neutral, 1 positive


# TextBlob (now with subjectivity parameter)
def textblob_fn (string, j, max_j, var="polr"):                        # Change polr to subj to get the subjectivity of the text
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if j == 0:
        print(f"TextBlob starts working at {time}")
    print(f"\rTextBlob working in speech {j} at {time}", end="")       # This reprint the line in the same space

    if var=="polr":
        tb_speech = TextBlob(string)
        result = round(tb_speech.polarity, 3)
    elif var== "subj":
        tb_speech = TextBlob(string)
        result = round(tb_speech.subjectivity, 3)
    else:
        print("Check spelling. Only polr or subj")
        result = np.nan
        
    time = now.strftime("%H:%M:%S")
    if j == max_j:
        print(f"\nTextBlob finished working at {time}")

    return result                   # -1 negative, 1 positive


# Vader
def vader_fn (string, j, max_j):
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    if j == 0:
        print(f"Vader starts working at {time}")
    print(f"\rVader working in speech {j} at {time}", end="")         # This reprint the line in the same space

    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(string)
    result = score["compound"]                                        # Author says that is the main statistic you need to see (-1 negative, 1 positive, between -0.05 and 0.05 neutral)

    time = now.strftime("%H:%M:%S")
    if j == max_j:
        print(f"\nVader finished working at {time}")

    return result
