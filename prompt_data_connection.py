import re

def connecting_prompts_with_news(prompt, news_art):
    # radio_mess = dataset.Radio_bodytext.tolist() # turns the radio messages into a list
    # news_arts = dataset.Nieuws_related_1_bodytext.tolist() # turns the news articles to a list
    # prompt_news_combi = []
    # prompts_same_length = []  # same length as prompts_news_combi. Contains solely the prompts
    
    pattern = r"(nieuwsbericht:\s*)"
    prompt_news_combi = re.sub(pattern, f"\g<1>{news_art} ", prompt)
    return prompt_news_combi

    #for news_art in news_arts:
        #pattern = r"(nieuwsbericht:\s*)"
       # prompt_news_combi = re.sub(pattern, f"\g<1>{news_art} ", prompt)
        #print(prompt_news_combi)   
        #prompt_news_combi.append(prompt + news_art)
    prompts_same_length.append(prompt)
    radio_mes_ext = []
    for radio_mes in radio_mess:
        radio_mes_ext.extend([radio_mes] * len(prompt_news_combi))


    return prompts_same_length, prompt_news_combi, radio_mes_ext

def connecting_prompt_with_gen_mess(lai_prompt, news_art, gen_mess):
    

    lai_combi = lai_prompt + f"Nieuwsbericht: {news_art}"
    counter = 0
    for i in gen_mess:
        counter += 1
        lai_combi = lai_combi + f"Output {counter}: {i} "

    return lai_combi


