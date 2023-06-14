import numpy as np
import pandas as pd
from data_processing import print_full
from ast import literal_eval
from constants import ls_eval_aspect, lm_model


def post_processing_1(df_3_cont):

    df_4_int = df_3_cont[["NA_index", f"{lm_model}_rm_i"]]
    col_names = []
    for aspect in ls_eval_aspect:
        df_3_cont[f'{lm_model}_{aspect}_ls'] = df_3_cont[f'{lm_model}_{aspect}_ls'].apply(literal_eval)
        df_4_int[f'{lm_model}_{aspect}_M'] = df_3_cont[f'{lm_model}_{aspect}_ls'].apply(lambda x: sum(x) / len(x)) 
        col_name = f'{lm_model}_{aspect}_M'
        col_names.append(col_name)

    df_4_int.loc[:,f"{lm_model}_eval_M"] = df_4_int.loc[:, col_names].mean(axis=1)
    df_4_int.loc[:, f"{lm_model}_ranking"] = df_4_int.groupby("NA_index")[f"{lm_model}_eval_M"].rank(ascending=1,method='dense')
    #print(df_4_int)
    

    return df_4_int
