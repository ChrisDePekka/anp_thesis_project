import re
from data_processing import print_full

def connecting_prompts_with_news(prompt, news_art):
    # radio_mess = dataset.Radio_bodytext.tolist() # turns the radio messages into a list
    # news_arts = dataset.Nieuws_related_1_bodytext.tolist() # turns the news articles to a list
    # prompt_news_combi = []
    # prompts_same_length = []  # same length as prompts_news_combi. Contains solely the prompts
    
    pattern = r"(nieuwsbericht:\s*)"
    prompt_news_combi = re.sub(pattern, f"\g<1>{news_art} ", prompt)
    return prompt_news_combi


def connecting_prompt_with_gen_mess(lai_prompt, news_art, gen_mess):
    

    lai_combi = lai_prompt + f"Nieuwsbericht: {news_art}"
    #print(lai_combi)
    counter = 0
    for i in gen_mess:
        counter += 1
        lai_combi = lai_combi + f"Output {counter}: {i} "

    return lai_combi


def connecting_clavie_prompt_with_gen_mess(input_clavie_eval_2, input_news, input_radios, lai_variant):
    lai_var_fin_combi = ''
    if lai_variant == True:
        
        lai_var_combi = input_clavie_eval_2+ f" Nieuwsbericht: {input_news}"
        #print(lai_combi)
        counter = 0
        ls_alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', "J", 'K']
        for i in input_radios:
            #counter += 1

            lai_var_fin_combi = lai_var_combi + f"Output {ls_alphabet[counter]}: {i} "
            lai_var_combi = lai_var_fin_combi
            counter += 1
            #print("lai var", lai_var_combi)
        return lai_var_fin_combi

    else:
        pattern = r"Nieuwsbericht: (.*)"
        replacement = r"Nieuwsbericht: " + input_news + r" \1"
        combi_with_news = re.sub(pattern, replacement, input_clavie_eval_2)
        pattern2 = r"Voor de volgende radioberichten: (.*)"
        replacement2 = r"Voor de volgende radioberichten: " + create_str_gen_rm(input_radios) + r" \1"
        final_cl_eval_prompt = re.sub(pattern2, replacement2, combi_with_news)
        #print_full(final_cl_eval_prompt)
        return final_cl_eval_prompt

def create_str_gen_rm( in_radios):
    #print(comb_w_news)
    #output_ls = []
    #empty_str = ''
    #print(in_radios)
    cl_eval_rm_combi = ''
    counter = -1
    for j in in_radios:
        counter += 1
        cl_eval_rm_combi += f"Radiobericht {counter}: {j} "
        #cl_eval_rm_combi += cl_eval_rm_combi

    return cl_eval_rm_combi