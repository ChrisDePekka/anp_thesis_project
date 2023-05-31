from generation_prompts import generate_prompts_clavie, generate_clavie_evaluation
from prompt_data_connection import connecting_prompts_with_news, connecting_prompt_with_gen_mess, connecting_clavie_prompt_with_gen_mess
import pandas as pd
from data_processing import print_full

# import variables
from constants import zero_cot, instructions, reit, right, info, name, pos, lm_model, n_g_r, ls_eval_aspect


def create_prompt_newsarticle(dataset):

    if lm_model == 'cl':
        mock = False
        clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos)
        print("those are the prompts: ", clavie_prompt1, clavie_prompt2, clavie_prompt3)
    else: # lm_model == 'gpt4'
        mock = True
        clavie_system_prompt, clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos)
        clavie_systems = pd.Series([clavie_system_prompt] * len(dataset))
    
    print(len(dataset))
    
    clavie_prompts1 = pd.Series([clavie_prompt1] * len(dataset))
    clavie_prompts3  = pd.Series([clavie_prompt3] * len(dataset))
    clavie_prompts2 = []
    #print(clavie_prompts1)
    for index, row in dataset.iterrows():
        conn_prompt2_news = connecting_prompts_with_news(clavie_prompt2, row[1])
        clavie_prompts2.append(conn_prompt2_news)

    if lm_model == 'gpt4': 
        dataset.loc[:, f'{lm_model}_system_prompt_0'] = clavie_systems
    dataset.loc[:, f'{lm_model}_prompt_1'] = clavie_prompts1
    dataset.loc[:, f'{lm_model}_prompt_2'] = clavie_prompts2
    dataset.loc[:, f'{lm_model}_prompt_3'] = clavie_prompts3
    # this can only be done if the index is the same. So when wanting to take other rows (not starting from 0 e.g.), then you first need to reset the index of the dataframe and only then you can do that.
    #print(dataset)
    return dataset

def create_eval_prompts(df_1):
    
    if lm_model == "cl":
        #print("See which columns I drop", print(df_1.columns))
        df_temp = df_1.drop(df_1.columns[2:6], axis=1)
    else:
        # one extra due to system prompt
        df_temp = df_1.drop(df_1.columns[2:7], axis=1)
    
    df_3_int = df_temp.drop(df_temp.columns[2:(2+n_g_r+1)], axis=1) # plus one since also the golden rm is used.

    counter = 0
    for eval_aspect in ls_eval_aspect:

        lai_like_prompt = generate_clavie_evaluation(eval_aspect)
        cl_eval_comb = []
        for index, row in df_temp.iterrows():
            lai_variant = True
            conn_clavie_eval_gen_radio = connecting_clavie_prompt_with_gen_mess(lai_like_prompt, row[1], row[2:], lai_variant)
            cl_eval_comb.append(conn_clavie_eval_gen_radio)
        
        df_3_int.loc[:, f'{eval_aspect}_e_prompt'] = cl_eval_comb
        
        #counter += (n_g_r+1) # plus one since also the golden rm is used
    return df_3_int