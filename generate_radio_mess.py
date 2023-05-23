import re
from LLM_generator import LLM_rm_generator, LLM_rms_evaluator, gpt_generator, gpt_evaluator
from data_processing import print_full
def generate_radio_messages(dataframe, n_g_r):
    ls_all_news_gen_mess = []
    print(dataframe.columns)
    print(len(dataframe))
    for index, row in dataframe.iterrows():
       
        ls_generated_mess_1_news = generate_messages_per_newsitem(row[3:7], n_g_r) # consists of a list including the 9 generated messages
        ls_all_news_gen_mess.append(ls_generated_mess_1_news)

        #print(ls_all_news_gen_mess)


    dataframe.loc[:, 'generated_mess'] = ls_all_news_gen_mess
    print(dataframe['generated_mess'])
    return dataframe

def generate_messages_per_newsitem(input_text, n_g_r):
    # systemprompt is input_text[0]
    # prompt1 is input_text[1]
    # prompt2 is input_text[2]
    # prompt3 is input_text[3]
    j = 0
    ls_generated_mess = []
    while j < n_g_r:
        # output 3 should be the final shortened radio message
        #output3 = LLM_rm_generator(input_text[0], input_text[1], input_text[2], input_text[3])
        
        output3 = gpt_generator(input_text[0], input_text[1], input_text[2], input_text[3])
        # output3 = 

        ls_generated_mess.append(output3) 
        j += 1
    return ls_generated_mess # must be returned the final_generated_message


def generate_radio_scores(dataframe, n_s, n_g_r):

    # create n_s new columns that each contain a list of the scores (the scores are the scores of all the n_g_r together)

    col_names = ['eval_scores_run_{}'.format(g+1) for g in range(n_s)]
    for col_name in col_names:
        dataframe[col_name] = None


    for index, row in dataframe.iterrows():
        print(dataframe.columns)


        ls_n_s = [generate_scores(row["evaluation_prompts"], n_s) for _ in range(n_s)] # a list containing lists. The inner lists are the scores of every radiomessage.

        # For this try, I will make the case when the list is empty (no scores are found)
        for i, inner_list in enumerate(ls_n_s):
            # Check if the inner list is empty
            if not inner_list:
                # Replace the empty inner list with a new list
                # is actually ["10", "20"], so pay attention
                ls_n_s[i] = [10, 20]

        for i, col_name in enumerate(col_names):
            print(col_name)
            dataframe.loc[index, col_name] = ls_n_s[i]


    # I am unsure whether this is the correct way. 
    # The goal: Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]
    # Weet niet of het zo klopt, maar lastig te controleren als je de output niet kent.
    col_names_per_radio_mes = []
    for g in range(n_g_r):
        print("heeeere")
        print(g)
        col_name_per_radio_mes = "eval_scores_gen_radio_mess_" + str(g+1)
        col_names_per_radio_mes.append(col_name_per_radio_mes )
        print(col_name_per_radio_mes)
    print(col_names_per_radio_mes)
    #content_scores_radio_mess = []

    for a in col_names_per_radio_mes:
        column_name = a
        dataframe.loc[:, column_name] = None







    counter = 0
    counter2 = 0
    while counter < n_g_r:

        for index, row in dataframe.iterrows():
           
            content_scores_radio_mess = []
            content_scores_radio_mess.extend([row[name_col][counter] for name_col in col_names]) # use extent instead of append otherwise you get a nested list

            dataframe.at[index, col_names_per_radio_mes[counter2]] = content_scores_radio_mess.copy()

        counter += 1 
        counter2 += 1


    print_full(dataframe[-2:][:])
    return dataframe, col_names_per_radio_mes

def generate_scores(eval_prompt, n_s):
    int_list = []
    
    while len(int_list) != n_s:  # rerun the evaluation prompt until you do get the wanted output.

        ls_scores_one_eval_run = []
        #output_LLM = LLM_rms_evaluator(eval_prompt)

        output_LLM = gpt_evaluator(eval_prompt)

        #output_LLM contains the entire output prompt in which the scores are given to the radio messages
    
        ls_scores_one_eval_run = re.findall(r"Score: (\d+)\nUitleg:\n(.+)", output_LLM)
    

        # turn into integers
        for num in ls_scores_one_eval_run:
            int_list.append(int(num))

    return int_list


    # since the radio-messages are in sequence, the first encountered score belongs to ls_n_r 1

        # Continue here, the question is how to take the scores.
        # I can use regular expression based on the numbers, or after Score 1: e.g. . 
        # Can make lists of the scores belonging to 1 radio message.

    # Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]