from generation_prompts import generate_prompts_clavie, generate_lai_eval_prompts, generate_clavie_evaluation
from prompt_data_connection import connecting_prompts_with_news, connecting_prompt_with_gen_mess, connecting_clavie_prompt_with_gen_mess
import pandas as pd
from data_processing import print_full

# import variables
from constants import zero_cot, instructions, mock, reit, right, info, name, pos
from constants import evaluate_aspect

def create_prompt_newsarticle(dataset):

    # for now:
    # At the moment I ignored system and user since don't know whether that will be available
    print("type: ", type(dataset))

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



    # dataset['cl_systemprompt'] = cl_system
    # dataset['cl_prompt1'] = cl_prompt1
    # dataset['cl_prompt2'] = cl_prompt2
    # dataset['cl_prompt3'] = cl_prompt3

    # print(dataset[:5])
    # print(dataset.columns)
    # print(dataset['cl_prompt2'][:5])
    # print_full(dataset)
    return dataset
    #print(prompts_same_length[:5], prompt_news_combi[:1], radio_mes_ext[:1])


def create_eval_prompts(dataframe, evaluate_aspect):
    lai_eval_prompt = generate_lai_eval_prompts()
    lai_prompt_comb = []

    system_prompt, cl_eval_prompt_1, cl_eval_prompt_2 = generate_clavie_evaluation(evaluate_aspect)
    cl_eval_comb = []
    print(cl_eval_prompt_2)
    

    for index, row in dataframe.iterrows():
        #print(row[1]) # is the news_article
        # I want to get the last column, since those contain the n generated messages
        #print("NEEEDT O LOOK FOOR THISSSSSS")
        
        #print(row[-1])
        conn_laiprompt_gen_radio = connecting_prompt_with_gen_mess(lai_eval_prompt, row[1] , row[-1])
        lai_prompt_comb.append(conn_laiprompt_gen_radio)

        conn_clavie_eval_gen_radio = connecting_clavie_prompt_with_gen_mess(cl_eval_prompt_2, row[1], row[-1])
        cl_eval_comb.append(conn_clavie_eval_gen_radio)
    
    dataframe.loc[:, 'evaluation_prompts'] = lai_prompt_comb
    print(dataframe['evaluation_prompts'])
    #dataframe['evaluation_prompts'] = lai_prompt_comb
    return dataframe