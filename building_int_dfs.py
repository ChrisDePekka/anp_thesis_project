from constants import lm_model, n_s, ls_eval_aspect

def create_df(dataframe):
    if lm_model == "cl":

        selected_columns_df = dataframe.drop(dataframe.columns[2:6], axis=1)
        df_2_int = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "cl_rm_i", value_name = "cl_rm_str")
    else:
        # one extra due to system prompt
        selected_columns_df = dataframe.drop(dataframe.columns[2:7], axis=1)
        df_2_int = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "gpt4_rm_i", value_name = "gpt4_rm_str")
    
    return df_2_int
    
    