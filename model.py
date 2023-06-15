from data_processing import get_data, print_full
from experiments import create_prompt_newsarticle, create_eval_prompts
from generate_radio_mess import generate_radio_messages, generate_radio_scores
from post_processing import post_processing_1
from building_int_dfs import create_df
#from prompt_data_connection import create_prompt_newsarticle
import pandas as pd
import config

# Import constants:
from constants import n_s, n_g_r, lm_model, ls_eval_aspect, path, path2


if __name__ == "__main__":

    a = 1
    if a == 1:


            #Import small dataset to test the prompts on
        dataset_to_generate, df_0 = get_data()

        df_0.to_csv(f'{lm_model}_exp_1_df_0_v2t.csv', index=False)
        #print_full(dataset_to_generate)
        print(df_0)

    #else:
        # # Use only the first row to show that it works
        sample_row_df = dataset_to_generate.iloc[4:6]
        #print(sample_row_df)
        sample_row_df = sample_row_df.reset_index(drop=True)
        
        # # dataframe including the prompt_newsarticle combination
        df_with_prompts_incl_prompt_news = create_prompt_newsarticle(sample_row_df)
        #df_with_prompts_incl_prompt_news = create_prompt_newsarticle(dataset_to_generate)

        print_full(df_with_prompts_incl_prompt_news)
        df_with_generated_radio = generate_radio_messages(df_with_prompts_incl_prompt_news)

        df_1 = df_with_generated_radio.copy()
        df_1.to_csv(f'{lm_model}_exp_1_df_1_v2t.csv', index=False)

    else:
    
        df_1_cont = pd.read_csv(f'{path2}/anp_thesis_project/{lm_model}_exp_1_df_1_v2t.csv', delimiter=',')

        
        df_2_int = create_df(df_1_cont)

        df_2 = create_eval_prompts(df_1_cont)

        df_2.to_csv(f'{lm_model}_exp_1_df_2_v2t.csv', index=False)


        print(df_2_int)
    #else:
        df_2_cont = pd.read_csv(f'{path2}/anp_thesis_project/{lm_model}_exp_1_df_2_v2t.csv', delimiter=',')
        
        


    #else:
        df_3 = generate_radio_scores(df_2_cont, df_2_int)
        df_3.to_csv(f'{lm_model}_exp_1_df_3_v2t.csv', index=False)
        
    #else:
        df_3_cont = pd.read_csv(f'{path2}/anp_thesis_project/{lm_model}_exp_1_df_3_v2t.csv', delimiter=',')

        df_4 = post_processing_1(df_3_cont)


        df_4_c = df_4.copy()
        df_4_c.to_csv(f'{lm_model}_exp_1_df_4_v2t.csv', index=False)
    
    
        



