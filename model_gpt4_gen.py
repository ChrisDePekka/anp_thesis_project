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

    # Use only the first row to show that it works
    sample_row_df = dataset_to_generate.iloc[0:2]


    # dataframe including the prompt_newsarticle combination
    df_with_prompts_incl_prompt_news = create_prompt_newsarticle(sample_row_df)
    #print(df_with_prompts_incl_prompt_news)
    # For now, it contains 1 column and each row contains a list of the 10 generated radio messages
    # could make separate columns out of it
    df_with_generated_radio = generate_radio_messages(df_with_prompts_incl_prompt_news, n_g_r)

    # evaluation prompt evaluating "vloeiendheid"
    aspect_to_evaluate = "vloeiendheid"
    df_with_evaluation_prompts = create_eval_prompts(df_with_generated_radio, aspect_to_evaluate)

    # evaluation prompt evaluating "relevantie"


    # evaluation prompt evaluating "feitelijkheid"

    # evaluation prompt evaluating "spreektaal"