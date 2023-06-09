import pandas as pd
from pandas import read_csv





def get_data(data_csv):

    path = "C:/Users/20183274/Documents/Scriptie/Thesis_Code_ANP"
    csv_file = data_csv
    df = pd.read_csv(f'{path}/data/{csv_file}', delimiter=',')  # of sep= ','

    selected_columns_df = df[["Radio_bodytext", "Nieuws_related_1_bodytext", "Nieuws_categorie"]]


    # remove rows that do not have Nieuws_categorie BIN, BUI, ECO, SPO # to fix

    # Create a copy of the selected columns DataFrame
    selected_columns_df_copy = selected_columns_df.copy()

    #   Apply preprocessing functions
    selected_columns_df_copy['Nieuws_related_1_bodytext'] = selected_columns_df_copy['Nieuws_related_1_bodytext'].apply(preprocess_input)
    selected_columns_df_copy['Radio_bodytext'] = selected_columns_df_copy['Radio_bodytext'].apply(preprocess_input)
    
    return selected_columns_df_copy





def preprocess_input(text):
    text = remove_text_before_dash(text)
    return text


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