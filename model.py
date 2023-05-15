from data_processing import get_data, print_full
from experiments import create_prompt_newsarticle, create_eval_prompts
from generate_radio_mess import generate_radio_messages, generate_radio_scores
from post_processing import post_processing
#from prompt_data_connection import create_prompt_newsarticle
import pandas as pd


# Import constants:
from constants import n_s, n_g_r, csv_file


if __name__ == "__main__":

    # Import small dataset to test the prompts on
    dataset_to_generate = get_data(csv_file)
    #print(dataset_to_generate[:5])

    #print_full(dataset_to_generate)
    #dataset_to_generate[:2].show()

    # Use only the first row to show that it works
    sample_row_df = dataset_to_generate.iloc[0:2]


    # dataframe including the prompt_newsarticle combination
    df_with_prompts_incl_prompt_news = create_prompt_newsarticle(sample_row_df)
    #print(df_with_prompts_incl_prompt_news)
    # For now, it contains 1 column and each row contains a list of the 10 generated radio messages
    # could make separate columns out of it
    df_with_generated_radio = generate_radio_messages(df_with_prompts_incl_prompt_news, n_g_r)
    print(df_with_generated_radio)
    
    a = 2

        # evaluation prompts
    df_with_evaluation_prompts = create_eval_prompts(df_with_generated_radio)
    print_full(df_with_evaluation_prompts)
    if a == 2:
        print("well")

    else:
        # generate the scores belonging to each generated radio-message.
        # This includes the following two types of columns
        # Type 1: consists of n_s runs and each column is a run, thus consisting of scores for the n_g_r messages
        # Type 2: consists of n_g_r columns and each column is a generated radio mess, thus consisting of n_s scores of the individual 
        # radio mess
        # col_names_scores contain the scores per radio message

        df_with_evaluation_scores, col_names_scores = generate_radio_scores(df_with_evaluation_prompts, n_s, n_g_r)

        # post processing dataframe
        # Step 1: create the mean of the scores per radio-mess, add this to a new column
        # Step 2: select the best generated radio mess by selecting the one with the highest mean.
        # Step 3: In the final two columns, place the found mean of the highest radio message, place the best-found generated radio-mess. 
        final_df_incl_best_found_output = post_processing(df_with_evaluation_scores, n_g_r, col_names_scores)

        print(final_df_incl_best_found_output)



