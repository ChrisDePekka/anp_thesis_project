from generation_prompts import generate_prompts_clavie, generate_lai_eval_prompts, generate_clavie_evaluation
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
        clavie_system = pd.Series([clavie_system_prompt] * len(dataset))
    
    clavie_prompt1 = pd.Series([clavie_prompt1] * len(dataset))
    clavie_prompt3  = pd.Series([clavie_prompt3] * len(dataset))
    clavie_prompt2 = []

    for index, row in dataset.iterrows():
        print(row[1]) # is the news_article
        print(clavie_prompt2)
        conn_prompt2_news = connecting_prompts_with_news(clavie_prompt2, row[1])
        clavie_prompt2.append(conn_prompt2_news)
    #print(cl_prompt2)

    #prompts_same_length, prompt_news_combi, radio_mes_ext = connecting_prompts_with_data(clavie_prompt2, dataset)

    print(dataset.columns)
    # dataset.loc[:, 'cl_systemprompt'] = cl_system better to use this
    if llm_name == 'gpt4': 
        dataset.loc[:, f'{llm_name}_systemprompt'] = clavie_system
    dataset.loc[:, f'{llm_name}_prompt1'] = clavie_prompt1
    dataset.loc[:, f'{llm_name}_prompt2'] = clavie_prompt2
    dataset.loc[:, f'{llm_name}_prompt3'] = clavie_prompt3


    return dataset
    #print(prompts_same_length[:5], prompt_news_combi[:1], radio_mes_ext[:1])


def create_eval_prompts(dataframe, ls_eval_aspects, lai_var):
    for eval_aspect in ls_eval_aspects:

        if lai_var == True:
            lai_eval_prompt = generate_lai_eval_prompts()
            lai_prompt_comb = []
        else:
            lai_like_prompt = generate_clavie_evaluation(eval_aspect)
            cl_eval_comb = []
        

        for index, row in dataframe.iterrows():
            if lai_var == True:
                conn_laiprompt_gen_radio = connecting_prompt_with_gen_mess(lai_eval_prompt, row[1] , row[-1])
                lai_prompt_comb.append(conn_laiprompt_gen_radio)
            else:
                lai_variant = True
                conn_clavie_eval_gen_radio = connecting_clavie_prompt_with_gen_mess(lai_like_prompt, row[1], row[-1], lai_variant)
                cl_eval_comb.append(conn_clavie_eval_gen_radio)
        
        if lai_var == True:
            dataframe.loc[:, f'{eval_aspect}_eval_prompt'] = lai_prompt_comb
            #print(dataframe['evaluation_prompts'])
        else:
            dataframe.loc[:, f'{eval_aspect}_eval_prompt'] = cl_eval_comb
            #print(dataframe['evaluation_prompts'])
    #dataframe['evaluation_prompts'] = lai_prompt_comb
    return dataframe