import re
from LLM_generator import LLM_rm_generator, LLM_rms_evaluator, gpt_generator, gpt_evaluator, claude_generator, claude_evaluator
from data_processing import print_full
def generate_radio_messages(dataframe, n_g_r, llm_model):

    

    ls_all_news_gen_mess = []
    print(dataframe.columns)
    print(len(dataframe))
    for index, row in dataframe.iterrows():
       i = 0
       while i < n_g_r:
            gen_rm = generate_message_per_newsitem(row[3:7], llm_model) # consists of a list including the 9 generated messages
            ls_all_news_gen_mess.append(gen_rm)

        #print(ls_all_news_gen_mess)

        #col_name_per_radio_mes = f"{eval_aspect}_eval_scores_gen_radio_mess_" + str(g+1)
        #col_names_per_radio_mes.append(col_name_per_radio_mes )

    dataframe.loc[:, 'generated_mess'] = ls_all_news_gen_mess
    print(dataframe['generated_mess'])
    return dataframe

def generate_message_per_newsitem(input_text, llm_model):
    if llm_model == 'cl':
        output3 = claude_generator(input_text[0], input_text[1], input_text[2], input_text[3])
    else:
        #output3 = LLM_rm_generator(input_text[0], input_text[1], input_text[2], input_text[3])
        output3 = gpt_generator(input_text[0], input_text[1], input_text[2], input_text[3])

    return output3 # must be returned the final_generated_message


def generate_radio_scores(dataframe, n_s, n_g_r, llm_model, ls_eval_aspects):

    # create n_s new columns that each contain a list of the scores (the scores are the scores of all the n_g_r together)
    for eval_aspect in ls_eval_aspects:
        col_names = [f'{eval_aspect}_eval_scores_run_{g+1}' for g in range(n_s)]
        for col_name in col_names:
            dataframe.loc[:, col_name] = None

        for index, row in dataframe.iterrows():

            ls_n_s = [generate_scores(row[f"{eval_aspect}_eval_prompt"], n_s, llm_model) for _ in range(n_s)] # a list containing lists. The inner lists are the scores of every radiomessage.

            # For this try, I will make the case when the list is empty (no scores are found)
            for i, inner_list in enumerate(ls_n_s):
                # Check if the inner list is empty
                if not inner_list:
                    # Replace the empty inner list with a new list
                    # is actually ["10", "20"], so pay attention
                    print(ls_n_s)
                    ls_n_s[i] = [10, 20]

            for i, col_name in enumerate(col_names):
                dataframe.at[index, col_name] = ls_n_s[i]
                # Need to use .at instead of .loc, since the column will first contain a list and second row None, which are two different
                # data types
                #dataframe.loc[index, col_name] = ls_n_s[i]


        # I am unsure whether this is the correct way. 
        # The goal: Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]
        # Weet niet of het zo klopt, maar lastig te controleren als je de output niet kent.

        # HOI
        col_names_per_radio_mes = []
        for g in range(n_g_r):

            col_name_per_radio_mes = f"{eval_aspect}_eval_scores_gen_radio_mess_" + str(g+1)
            col_names_per_radio_mes.append(col_name_per_radio_mes )
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


    #print_full(dataframe[-2:][:])
    return dataframe, col_names_per_radio_mes

def generate_scores(eval_prompt, n_s, llm_model):
    int_list = []
    
    while len(int_list) != n_s:  # rerun the evaluation prompt until you do get the wanted output.

        ls_scores_one_eval_run = []
        #output_LLM = LLM_rms_evaluator(eval_prompt)
        if llm_model == 'Claude':
            output_LLM = claude_evaluator(eval_prompt)
        else:
            output_LLM = gpt_evaluator(eval_prompt)

        #output_LLM contains the entire output prompt in which the scores are given to the radio messages
        #ls_scores_one_eval_run = re.findall(r"Score: (\d+)\nUitleg:\n(.+)", output_LLM)
        ls_scores_one_eval_run = re.findall(r"Score.*?(\d+)", output_LLM)
        # numbers = re.findall(r"Score\D*(\d+)", output_LLM)
    

        # turn into integers
        for num in ls_scores_one_eval_run:
            int_list.append(int(num))
    print("length:", len(int_list))
    return int_list


    # since the radio-messages are in sequence, the first encountered score belongs to ls_n_r 1

        # Continue here, the question is how to take the scores.
        # I can use regular expression based on the numbers, or after Score 1: e.g. . 
        # Can make lists of the scores belonging to 1 radio message.

    # Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]