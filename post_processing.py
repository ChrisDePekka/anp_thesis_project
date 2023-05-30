import numpy as np
import pandas as pd
from data_processing import print_full
from ast import literal_eval


def post_processing_1(df_3_cont, eval_aspects, llm):

    if llm == 'Claude':
        lm = 'cl'
    else:
        lm = 'gpt'

    df_4_int = df_3_cont[["NA_index", f"{lm}_rm_i"]]
    col_names = []
    for aspect in eval_aspects:
        df_3_cont[f'{lm}_{aspect}_ls'] = df_3_cont[f'{lm}_{aspect}_ls'].apply(literal_eval)
        df_4_int[f'{lm}_{aspect}_M'] = df_3_cont[f'{lm}_{aspect}_ls'].apply(lambda x: sum(x) / len(x)) 
        col_name = f'{lm}_{aspect}_M'
        col_names.append(col_name)

    df_4_int.loc[:,f"{lm}_eval_M"] = df_4_int.loc[:, col_names].mean(axis=1)
    df_4_int.loc[:, f"{lm}_ranking"] = df_4_int.groupby("NA_index")[f"{lm}_eval_M"].rank(ascending=1,method='dense')
    print(df_4_int)
    

    return df_4_int
