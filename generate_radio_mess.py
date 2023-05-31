import re
from LLM_generator import LLM_rm_generator, LLM_rms_evaluator, gpt_generator, gpt_evaluator, claude_generator, claude_evaluator
from data_processing import print_full
from constants import lm_model, n_g_r, n_s, lm_model, ls_eval_aspect

def generate_radio_messages(dataframe):

    ls_rms = []
    for n in range(n_g_r):
        ls_rm = f"{lm_model}_rm_{n+1}" 
        ls_rms.append(ls_rm)
    
    for col_name in ls_rms:
        dataframe.loc[:, col_name] = None
    print(dataframe.columns)
    for index, row in dataframe.iterrows():
       i = 0
       while i < n_g_r:
            print_full(dataframe)
            if lm_model == 'cl':
                
                gen_rm = generate_message_per_newsitem(row[3:7]) # row[3:7] are the input prompts, but for gpt4 there is an extra column (system_prompt) so needs to go to row :8
            else:
                gen_rm = generate_message_per_newsitem(row[3:8])
            i += 1
            dataframe.loc[index, f'{lm_model}_rm_{i}'] = gen_rm
            
            # Still need to add the cl_rm_g as a column
            # dataframe.loc[index, f'{lm_model}_rm_{i}'] = gen_rm
    dataframe.loc[:, f'{lm_model}_rm_g'] = dataframe['rm_g']
    return dataframe

def generate_message_per_newsitem(input_text):
    if lm_model == 'cl':
        print(input_text)
        output3 = claude_generator(input_text[0], input_text[1], input_text[2], input_text[3])
    else:
        #output3 = LLM_rm_generator(input_text[0], input_text[1], input_text[2], input_text[3])
        output3 = gpt_generator(input_text[0], input_text[1], input_text[2], input_text[3], input_text[4]) # input_text[0] is the system prompt

    return output3 # must be returned the final_generated_message


def generate_radio_scores(df_2, df_2_int):

    for eval_aspect in ls_eval_aspect:
        col_name = [f'{lm_model}_{eval_aspect}_ls']
        df_2_int.loc[:, col_name] = None


    for eval_aspect in ls_eval_aspect:

        col_name = [f'{eval_aspect}_R_s'] 
                
        df_2.loc[:, col_name] = None

        for index, row in df_2.iterrows():
            #print("what is the input", row[f'{eval_aspect}_e_prompt'])
            ls_n_s = [generate_scores(row[f"{eval_aspect}_e_prompt"], n_g_r, lm_model) for _ in range(n_s)] 
            # this does n_s runs
            # a list containing lists. The inner lists are the scores of every radiomessage.
            # So the function generate_scores returns a list containing n_g_r int (scores)
            i = 0
            j = 1
            while i <= (n_g_r+1): # i # 2 <= 4 # 3 <= 4  5 <= 4 # j 0 j 1 
                ls_scores_rm = [run[i] for run in ls_n_s] # 70 80 85
                if i == n_g_r:
                    i = 'g'
                    j = '' # j is needed since you cannot add 1 to g, 1 needed to be added since radio-message starts from 1.

                row_index = df_2_int.index[(df_2_int["NA_index"] == row["NA_index"]) & (df_2_int["cl_rm_i"] == f'{lm_model}_rm_{i+j}')].tolist()
                df_2_int.at[row_index[0], f'{lm_model}_{eval_aspect}_ls'] = ls_scores_rm
                
                if i == 'g':
                    i = n_g_r + 2
                else:
                    i += 1
                   
            #df_3_int.at[index, col_name] = ls_n_s # it unfortunately does not let me insert a list of lists into one cell.
    df_2_int = df_2_int.sort_values(by=["NA_index"])
    df_2 = df_2_int.copy()
    return df_2

def generate_scores(eval_prompt, n_g_r):
    int_list = []

    # bij relevantie prompt gaat mis
    while len(int_list) != (n_g_r+1):  # rerun the evaluation prompt until you do get the wanted output.
        int_list = []
        ls_scores_one_eval_run = []
        #output_LLM = LLM_rms_evaluator(eval_prompt)

        if lm_model == 'Claude':
            output_LLM = claude_evaluator(eval_prompt)
        else:
            output_LLM = gpt_evaluator(eval_prompt)
                
        ls_scores_one_eval_run = re.findall(r"Score.*?(\d+)", output_LLM)
        #ls_scores_one_eval_run = ['70', '80', '85']
        
        #output_LLM contains the entire output prompt in which the scores are given to the radio messages
        #ls_scores_one_eval_run = re.findall(r"Score: (\d+)\nUitleg:\n(.+)", output_LLM)

        # numbers = re.findall(r"Score\D*(\d+)", output_LLM)

        # turn into integers
        for num in ls_scores_one_eval_run:
            int_list.append(int(num))


    return int_list
