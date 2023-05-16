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
        col_name_mean_per_radio_mes = "eval_scores_mean_radio_mess_" + str(g+1)
        col_names_mean_per_radio_mes.append(col_name_mean_per_radio_mes)

    # Loop over the dataframe row by row, for each row 
    counter = 0
    counter2 = 0
    mean_score_per_radio_mess = []
    while counter < n_g_r:
        for index, row in df.iterrows():
            print(row['eval_scores_run_1'])
            for name_col in col_names_scores:
                print(type(row[name_col]))
                print(row[name_col])
                a = np.mean(row[name_col])
                print(a)
                mean_score_per_radio_mess.append(a)

            #mean_score_per_radio_mess.append([np.mean(row[col_name]) for col_name in col_names_scores])
            #mean_score_per_radio_mess.append([row[col_name].apply(mean_func) for col_name in col_names_scores])
                print(mean_score_per_radio_mess)

            df[col_names_mean_per_radio_mes[counter2]] = mean_score_per_radio_mess

            mean_score_per_radio_mess.clear()
        counter += 1 
        counter2 += 1


    # Select the radio message with the highest mean value
    max_func = lambda x: max([int(i) for i in x])
    #max_func_col = lambda x: df.columns[x.argmax()][-n_g_r:]
    max_func_col = lambda x: x.idxmax()
    #max_func = lambda x: max(x)
    print("BE MORE VISIBLE")
    print_full(df.iloc[:, -n_g_r:])
    print(type(df.iloc[:, -n_g_r:]))
    print(df.iloc[:, -n_g_r:])
    df.loc[:, 'highest_mean_score'] = df.iloc[:,-n_g_r:].apply(max_func, axis=1)
    df.loc[:, 'highest_mean_score_col_name'] = df.iloc[:,-n_g_r:].apply(max_func_col, axis=1)
    #print(df['highest_mean_col'])

    # split the 'highest_mean_col' column into two separate columns
    # create a dataframe from the tuple containing the highest_mean_score and its corresponding dataframe
    #df[['highest_mean_score', 'highest_mean_score_col_name']] = pd.DataFrame(df['highest_mean_col'].tolist(), index=df.index)
    print("Show me this:2 ", df["highest_mean_score"])    
    print("Show me this: ", df["highest_mean_score_col_name"])
    highest_ranked_rm_ls = []

    for index, row in df.iterrows():
        col_rm_name = row['highest_mean_score_col_name']
        print("Final")
        print(row['highest_mean_score_col_name'])
        rm_nr = col_rm_name[-1]
        print("rm_nr: ", rm_nr)
        # the column with the generated messages is a list of the generated messages
        int_rm_nr = int(rm_nr)
        print(type(rm_nr))
        highest_ranked_rm = df.loc[index, 'generated_mess'][int_rm_nr-1]

        highest_ranked_rm_ls.append(highest_ranked_rm)


    df["best_gen_rm"] = highest_ranked_rm_ls
    print(df["best_gen_rm"])
    return df





