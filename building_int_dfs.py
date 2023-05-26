

def create_df(dataframe, ls_eval_aspects, n_s, llm):
    if llm == "Claude":

        selected_columns_df = dataframe.drop(dataframe.columns[2:6], axis=1)
        df_2_int = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "cl_rm_i", value_name = "cl_rm_str")
    else:
        # one extra due to system prompt
        selected_columns_df = dataframe.drop(dataframe.columns[2:7], axis=1)
        df_2_int = selected_columns_df.melt(id_vars = ["NA_index", "news_articles"], var_name = "gpt4_rm_i", value_name = "gpt4_rm_str")
    
    if llm == "Claude":
        lm = 'cl'
    else:
        lm = 'gpt4'

    # for eval_aspect in ls_eval_aspects:
    #     col_names = [f'{lm}_rm_{g+1}_{eval_aspect}' for g in range(n_s)]
    # for col_name in col_names:
    #     df_2_int.loc[:, col_name] = None
     
    

    print(df_2_int)
    print(df_2_int.columns)
    return df_2_int
    
    