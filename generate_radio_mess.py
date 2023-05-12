import re
from LLM_generator import science_tutoring

def generate_radio_messages(dataframe, n_g_r):

    ls_all_news_gen_mess = []
    #print(dataframe)

    for index, row in dataframe.iterrows():
        model_call = "here_we_call_PALM"

        # Here we call PALM on first prompt1
        
        #print(row[3])
        #print(row[3:6])

        
        ls_generated_mess_1_news = generate_messages_per_newsitem(row[3:6], n_g_r) # consists of a list including the 9 generated messages
        ls_all_news_gen_mess.append(ls_generated_mess_1_news)



    dataframe['generated_mess'] = ls_all_news_gen_mess
    return dataframe


def generate_messages_per_newsitem(input_text, n_g_r):
    # prompt1 is input_text[0]
    # prompt2 is input_text[1]
    # prompt3 is input_text[2]
    j = 0
    ls_generated_mess = []
    while j < n_g_r:
        # output 3 should be the final shortened radio message
        output3 = science_tutoring(input_text[0], input_text[1], input_text[2])
        ls_generated_mess.append(output3) # non-string ofc.

    return ls_generated_mess # must be returned the final_generated_message




def generate_radio_scores(dataframe, n_s, n_g_r):

    # create n_s new columns that each contain a list of the scores (the scores are the scores of all the n_g_r together)

    col_names = ['eval_scores_run_{}'.format(g+1) for g in range(n_s)]
    for col_name in col_names:
        dataframe[col_name] = None


    for index, row in dataframe.iterrows():
       
        ls_n_s = [generate_scores(row["evaluation prompts"]) for _ in range(n_s)] # a list containing lists. The inner lists are the scores of every radiomessage.

        for i, col_name in enumerate(col_names):
            dataframe.loc[index, col_name] = ls_n_s[i]



    # I am unsure whether this is the correct way. 
    # The goal: Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]
    # Weet niet of het zo klopt, maar lastig te controleren als je de output niet kent.
    col_names_per_radio_mes = []
    for g in range(n_s):
        col_name_per_radio_mes = "eval_scores_gen_radio_mess_" + str(g)
        col_names_per_radio_mes.append(col_name_per_radio_mes )

    content_scores_radio_mess = []
    counter = 0
    counter2 = 0
    while counter < n_g_r:
        for index, row in dataframe.iterrows():
            #print(index, row)
            # access the first element of each column and append it to the col_radio_mess list
            #content_scores_radio_mess.append([row['shuf_cl'][counter], row['shuf_c2'][counter], row['shuf_c3'][counter]])
            content_scores_radio_mess.append([row[col_name][counter] for col_name in col_names])
            print(content_scores_radio_mess)
        #df['new_col'] = new_col
        dataframe[col_names_per_radio_mes[counter2]] = content_scores_radio_mess
        content_scores_radio_mess.clear()
        counter += 1 
        counter2 += 1



    return dataframe, col_names_per_radio_mes

def generate_scores(eval_prompt):
    model_call = "here_we_call_PALM"
    # Here we call PALM on eval_prompt
    # completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=60)
    # message = completions.choices[0].text.strip()


    #output is one eval run, so that contains the scores of all the generated messages
    output_eval =  'palm generated'
    ls_scores_one_eval_run = re.findall(r"Score: (\d+)\nUitleg:\n(.+)", output_eval)
    return ls_scores_one_eval_run


    # since the radio-messages are in sequence, the first encountered score belongs to ls_n_r 1

        # Continue here, the question is how to take the scores.
        # I can use regular expression based on the numbers, or after Score 1: e.g. . 
        # Can make lists of the scores belonging to 1 radio message.


    
    # Now I want to take the mean of each Output



    # I am going to do: generate 



    # Maybe need to empty the lists first 


    # Heb dus een de columns met [radio_1-score, radio2 score, radio3 score], wil maken [radio1score, radio1 score, radio1score]