from generation_prompts import generate_prompts_clavie, generate_lai_eval_prompts, generate_clavie_evaluation
from prompt_data_connection import connecting_prompts_with_news, connecting_prompt_with_gen_mess, connecting_clavie_prompt_with_gen_mess
import pandas as pd
from data_processing import print_full

# import variables
from constants import zero_cot, instructions, reit, right, info, name, pos


def create_prompt_newsarticle(dataset, llm_model):

    # for now:
    # At the moment I ignored system and user since don't know whether that will be available
    print("type: ", type(dataset))
    if llm_model == 'Claude':
        mock = False
        clavie_system_prompt, clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos)
    else:
        mock = True
        clavie_system_prompt, clavie_prompt1, clavie_prompt2, clavie_prompt3 = generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos)
    
    # print(clavie_prompt1)
    # print(clavie_prompt2)
    # print(clavie_prompt3)

    cl_system = pd.Series([clavie_system_prompt] * len(dataset))
    cl_prompt1 = pd.Series([clavie_prompt1] * len(dataset))
    cl_prompt3  = pd.Series([clavie_prompt3] * len(dataset))
    cl_prompt2 = []

    for index, row in dataset.iterrows():
        #print(row[1]) # is the news_article
        conn_prompt2_news = connecting_prompts_with_news(clavie_prompt2, row[1])
        cl_prompt2.append(conn_prompt2_news)
    #print(cl_prompt2)

    #prompts_same_length, prompt_news_combi, radio_mes_ext = connecting_prompts_with_data(clavie_prompt2, dataset)

    print(dataset.columns)
    # dataset.loc[:, 'cl_systemprompt'] = cl_system better to use this 
    dataset.loc[:, 'cl_systemprompt'] = cl_system
    dataset.loc[:, 'cl_prompt1'] = cl_prompt1
    dataset.loc[:, 'cl_prompt2'] = cl_prompt2
    dataset.loc[:, 'cl_prompt3'] = cl_prompt3


    return dataset
    #print(prompts_same_length[:5], prompt_news_combi[:1], radio_mes_ext[:1])


def create_eval_prompts(dataframe, evaluate_aspect, lai_var):
    if lai_var == True:
        lai_eval_prompt = generate_lai_eval_prompts()
        lai_prompt_comb = []
    else:
        lai_like_prompt = generate_clavie_evaluation(evaluate_aspect)
        cl_eval_comb = []
    

    for index, row in dataframe.iterrows():
        if lai_var == True:
            conn_laiprompt_gen_radio = connecting_prompt_with_gen_mess(lai_eval_prompt, row[1] , row[-1])
            lai_prompt_comb.append(conn_laiprompt_gen_radio)
        else:

            conn_clavie_eval_gen_radio = connecting_clavie_prompt_with_gen_mess(lai_like_prompt, row[1], row[-1])
            cl_eval_comb.append(conn_clavie_eval_gen_radio)
    
    if lai_var == True:
        dataframe.loc[:, 'evaluation_prompts'] = lai_prompt_comb
        print(dataframe['evaluation_prompts'])
    else:
        dataframe.loc[:, 'evaluation_prompts'] = cl_eval_comb
        print(dataframe['evaluation_prompts'])
    #dataframe['evaluation_prompts'] = lai_prompt_comb
    return dataframe