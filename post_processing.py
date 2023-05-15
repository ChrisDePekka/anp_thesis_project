import numpy as np
import pandas as pd
from data_processing import print_full

def post_processing(df, n_g_r, col_names_scores):
    mean_func = lambda x: np.mean(x)


    # I might be able to replace this function by a quicker variant using this:
    #df['mean_col'] = df[-n_g_r:].apply(mean_func)
    # Only need to change mean_col by multiple column names (in a small for-loop)

    # Create the columns that will contain the mean of the generated radiomessages
    col_names_mean_per_radio_mes = []
    for g in range(n_g_r):
        col_name_mean_per_radio_mes = "eval_scores_mean_radio_mess_" + str(g)
        col_names_mean_per_radio_mes.append(col_name_mean_per_radio_mes)

    # Loop over the dataframe row by row, for each row 
    counter = 0
    counter2 = 0
    mean_score_per_radio_mess = []
    while counter < n_g_r:
        for index, row in df.iterrows():
            print(row['eval_scores_run_1'])

            mean_score_per_radio_mess.append([np.mean(row[col_name]) for col_name in col_names_scores])
            #mean_score_per_radio_mess.append([row[col_name].apply(mean_func) for col_name in col_names_scores])


        df[col_names_mean_per_radio_mes[counter2]] = mean_score_per_radio_mess
        mean_score_per_radio_mess.clear()
        counter += 1 
        counter2 += 1


    #print_full(df["eval_scores_mean_radio_mess_0"])


    # Select the radio message with the highest mean value
    max_func = lambda x: max([int(i) for i in x])

    #max_func = lambda x: max(x)
    print("BE MORE VISIBLE")
    print_full(df.iloc[:, -n_g_r:])
    print(type(df.iloc[:, -n_g_r:]))
    df['highest_mean_col'] = df.iloc[:,-n_g_r:].apply(max_func, axis=1)
    

    # split the 'max_col' column into two separate columns
    # create a dataframe from the tuple containing the highest_mean_score and its corresponding dataframe
    df[['highest_mean_score', 'highest_mean_score_col_name']] = pd.DataFrame(df['highest_mean_col'].tolist(), index=df.index)    

    highest_ranked_rm_ls = []

    for index, row in df.iterrows():
        col_rm_name = row['highest_mean_score_col_name']
        rm_nr = col_rm_name[-1]
        # the column with the generated messages is a list of the generated messages, therefore (starts from 0), so rm_nr must be minus 1
        highest_ranked_rm = df.loc[index, 'generated_mess'][rm_nr-1]

        highest_ranked_rm_ls.append(highest_ranked_rm)


    df["best_gen_rm"] = highest_ranked_rm_ls





