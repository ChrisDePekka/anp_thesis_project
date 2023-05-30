from data_processing import get_data, print_full
from experiments import create_prompt_newsarticle, create_eval_prompts
from generate_radio_mess import generate_radio_messages, generate_radio_scores
from post_processing import post_processing_1
from building_int_dfs import create_df
#from prompt_data_connection import create_prompt_newsarticle
import pandas as pd
import config

# Import constants:
from constants import n_s, n_g_r, csv_file, lm_model, ls_eval_aspect, path


if __name__ == "__main__":

    #THIS WORKS, FOR NOW I COMMENT IT OUT AND GO ON WITH THE CSV FILE
    #Import small dataset to test the prompts on
    dataset_to_generate, df_0 = get_data(csv_file)
    df_0.to_csv('new1_news_articles.csv', index=False)
    print_full(dataset_to_generate)
    a = 1
    if a == 1:
        print('hi')
    else:
        # # Use only the first row to show that it works
        sample_row_df = dataset_to_generate.iloc[0:2]
        
        # # dataframe including the prompt_newsarticle combination
        df_with_prompts_incl_prompt_news = create_prompt_newsarticle(sample_row_df)

        df_with_generated_radio = generate_radio_messages(df_with_prompts_incl_prompt_news)

        df_1 = df_with_generated_radio.copy()
        df_1.to_csv('new1_result_generation.csv', index=False)

        #UNTIL HEREEEE

        # THIS WORKS FOR NOW I COMMENT IT OUT AND GO ON WITH THE CSV FILE
        #else:
        df_1_cont = pd.read_csv(f'{path}/anp_thesis_project/new_result_generation.csv', delimiter=',')

        
        
        df_2_int = create_df(df_1_cont, ls_eval_aspect)

        df_2 = create_eval_prompts(df_1_cont, ls_eval_aspect)
        # .sort_values(by=["NA_index"])
        df_2.to_csv('new_df2_result.csv', index=False)
        df_2_cont = pd.read_csv(f'{path}/anp_thesis_project/new_df2_result.csv', delimiter=',')
        df_3 = generate_radio_scores(df_2_cont, df_2_int, n_s, n_g_r, lm_model, ls_eval_aspect)

        df_3.to_csv('fa_df3_result.csv', index=False)
        #UNTIL HEREEEE

    

        df_3_cont = pd.read_csv(f'{path}/anp_thesis_project/fa_df3_result.csv', delimiter=',')

        df_4 = post_processing_1(df_3_cont, ls_eval_aspect, lm_model)


        df_4_c = df_4.copy()
        df_4_c.to_csv('new_df4_result.csv', index=False)



