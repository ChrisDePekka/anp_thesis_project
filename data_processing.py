import pandas as pd
import re
from pandas import read_csv

def get_data(data_csv):

    path = "C:/Users/20183274/Documents/Scriptie/Thesis_Code_ANP"
    csv_file = data_csv
    df = pd.read_csv(f'{path}/data/{csv_file}', delimiter=',')  # of sep= ','
    
    df_0_temp = df[["Nieuws_related_1_bodytext", "Nieuws_related_1_title", "Nieuws_id"]]
    df_0_temp = df_0_temp.rename(columns={'Nieuws_related_1_bodytext': 'news_articles', "Nieuws_related_1_title": "news_titles", "Nieuws_id": 'news_ids'})
    df_0_temp2 = df_0_temp.copy()
    df_0_temp2["news_articles"] = df_0_temp2["news_articles"].apply(preprocess_input)
    df_0_temp2['NA_index'] = df_0_temp2.index
    df_0 = df_0_temp2[['NA_index','news_articles', 'news_titles', 'news_ids']]



    selected_columns_df = df[[ "Nieuws_related_1_bodytext", "Radio_bodytext"]]
    selected_columns_df = selected_columns_df.rename(columns={'Nieuws_related_1_bodytext': 'news_articles', "Radio_bodytext": "rm_g"})

    # Create a copy of the selected columns DataFrame
    df_to_use = selected_columns_df.copy()

    #   Apply preprocessing functions
    df_to_use["news_articles"] = df_to_use["news_articles"].apply(preprocess_input)
    df_to_use["rm_g"] = df_to_use["rm_g"].apply(preprocess_input)
    df_to_use['NA_index'] = df_to_use.index

    df_return = df_to_use[['NA_index','news_articles', 'rm_g']]
    return df_return, df_0


def preprocess_input(text):
    text = remove_text_before_dash(text)
    text2 = re.sub("</?p[^>]*>", "", text)
    return text2


def remove_text_before_dash(text):
    if ') -' in text:               # I check whether )space is before the dash, since it could be that it merely connects words.
                                    # by doing this, those dashes are not impacted
        text = text.split('-', 1)[1].strip()  # I remove everything standing before the dash.
    return text


def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')