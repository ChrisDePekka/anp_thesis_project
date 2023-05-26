from generation_prompts import generate_prompts_clavie, generate_clavie_evaluation
from prompt_data_connection import connecting_prompts_with_news, connecting_prompt_with_gen_mess, connecting_clavie_prompt_with_gen_mess
import pandas as pd
from data_processing import print_full

# import variables
from constants import zero_cot, instructions, reit, right, info, name, pos


def create_prompt_newsarticle(dataset, llm_model):

    if llm_model == 'Claude':
        mock = False
        llm_name = 'cl'
        clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos, llm_name)
    else:
        mock = True
        llm_name = 'gpt4'
        clavie_system_prompt, clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos, llm_name)
        clavie_systems = pd.Series([clavie_system_prompt] * len(dataset))
    
    clavie_prompts1 = pd.Series([clavie_prompt1] * len(dataset))
    clavie_prompts3  = pd.Series([clavie_prompt3] * len(dataset))
    clavie_prompts2 = []

    for index, row in dataset.iterrows():
        conn_prompt2_news = connecting_prompts_with_news(clavie_prompt2, row[1])
        clavie_prompts2.append(conn_prompt2_news)

    if llm_name == 'gpt4': 
        dataset.loc[:, f'{llm_name}_system_prompt_0'] = clavie_systems
    dataset.loc[:, f'{llm_name}_prompt_1'] = clavie_prompts1
    dataset.loc[:, f'{llm_name}_prompt_2'] = clavie_prompts2
    dataset.loc[:, f'{llm_name}_prompt_3'] = clavie_prompts3

    return dataset

def create_eval_prompts(dataframe, ls_eval_aspects, n_g_r, llm):
 
    if llm == "Claude":
        df_temp = dataframe.drop(dataframe.columns[2:6], axis=1)
    else:
        # one extra due to system prompt
        df_temp = dataframe.drop(dataframe.columns[2:7], axis=1)

    df_3 = df_temp.drop(df_temp.columns[2:(2+n_g_r+1)], axis=1) # plus one since also the golden rm is used.
    print(df_3)
    counter = 0
    for eval_aspect in ls_eval_aspects:

        lai_like_prompt = generate_clavie_evaluation(eval_aspect)
        cl_eval_comb = []
        
        for index, row in df_temp.iterrows():
            lai_variant = True
            #print("willing to see whats happening", row[6])
            #print(row)
            # row[1] is news article
            # row[6] is radiomessage 1
            #print("whats this", row[1])
            #print("need to know the input", row[6:])
            conn_clavie_eval_gen_radio = connecting_clavie_prompt_with_gen_mess(lai_like_prompt, row[1], row[6 + counter:], lai_variant)
            cl_eval_comb.append(conn_clavie_eval_gen_radio)
        
        df_3.loc[:, f'{eval_aspect}_e_prompt'] = cl_eval_comb
        
        counter += (n_g_r+1) # plus one since also the golden rm is used
    return df_3