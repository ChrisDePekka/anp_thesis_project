from data_processing import get_data, print_full
from experiments import create_prompt_newsarticle, create_eval_prompts
from generate_radio_mess import generate_radio_messages, generate_radio_scores
from post_processing import post_processing
#from prompt_data_connection import create_prompt_newsarticle
import pandas as pd
import config

# Import constants:
from constants import n_s, n_g_r, csv_file


if __name__ == "__main__":
    lm_model = "Claude"

    # THIS WORKS, FOR NOW I COMMENT IT OUT AND GO ON WITH THE CSV FILE
    # Import small dataset to test the prompts on
    # dataset_to_generate = get_data(csv_file)

    # # Use only the first row to show that it works
    # sample_row_df = dataset_to_generate.iloc[0:2]
    
    # # dataframe including the prompt_newsarticle combination
    # df_with_prompts_incl_prompt_news = create_prompt_newsarticle(sample_row_df, lm_model)

    # df_with_generated_radio = generate_radio_messages(df_with_prompts_incl_prompt_news, n_g_r, lm_model)

    # intermediate_gen_mess_result_df = df_with_generated_radio
    # intermediate_gen_mess_result_df.to_csv('final_result_generation.csv', index=False)

    # UNTIL HEREEEE

    path = "C:/Users/20183274/Documents/Scriptie/"
    df_1 = pd.read_csv(f'{path}/anp_thesis_project/final_result_generation.csv', delimiter=',')


    lai = False

    # eval_aspect variable is not needed anymore

    ls_eval_aspect = ["feit", "vloe", "rele", "spre"]
    # evaluation prompts
    df_2 = create_eval_prompts(df_1, ls_eval_aspect, lai)
    print(df_2)
    print(df_2.columns)

    #print_full(df_with_evaluation_prompts)

    # generate the scores belonging to each generated radio-message.
    # This includes the following two types of columns
    # Type 1: consists of n_s runs and each column is a run, thus consisting of scores for the n_g_r messages
    # Type 2: consists of n_g_r columns and each column is a generated radio mess, thus consisting of n_s scores of the individual 
    # radio mess
    # col_names_scores contain the scores per radio message

    df_with_evaluation_scores = generate_radio_scores(df_2, n_s, n_g_r, lm_model, ls_eval_aspect)
    print_full(df_with_evaluation_scores)
    print(df_with_evaluation_scores.columns)
    intermediate_result_eval = df_with_evaluation_scores
    intermediate_result_eval.to_csv('int_eval_scores_df.csv', index=False)
    a = 1
    if a == 1:
        print('stop')
    else:
        # post processing dataframe
        # Step 1: create the mean of the scores per radio-mess, add this to a new column
        # Step 2: select the best generated radio mess by selecting the one with the highest mean.
        # Step 3: In the final two columns, place the found mean of the highest radio message, place the best-found generated radio-mess. 
        final_df_incl_best_found_output = post_processing(df_with_evaluation_scores, n_g_r, col_names_scores, ls_eval_aspect)

        final_df_incl_best_found_output.to_csv('final_ten_results.csv', index=False)

        #print_full(final_df_incl_best_found_output)




