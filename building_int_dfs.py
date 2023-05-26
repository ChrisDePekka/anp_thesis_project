

def create_df(dataframe, llm):
    if llm == "Claude":

        selected_columns_df = dataframe.drop(dataframe.columns[2:6], axis=1)
        df_2 = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "cl_rm_i", value_name = "cl_rm_str")
    else:
        # one extra due to system prompt
        selected_columns_df = dataframe.drop(dataframe.columns[2:7], axis=1)
        df_2 = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "gpt4_rm_i", value_name = "gpt4_rm_str")
    
    return df_2
    
    