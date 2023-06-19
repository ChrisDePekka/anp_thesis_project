#from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from data_processing import get_data
from constants import examples, csv_file, n_of_examples
import openai
from config import api_key_1, api_key_gpt
import asyncio
import os
import anthropic
import time
import re



def LLM_rm_generator(input_system_prompt, input_prompt1, input_prompt2, input_prompt3, temperature=.2):

    #chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,    # Token limit determines the maximum amount of text output.
        "top_p": 0.95,               # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,                 # A top_k of 1 means the selected token is the most probable among all tokens.
    }


    if n_of_examples > 0:
        df = get_data(csv_file)
        random_rows = df.sample(n=n_of_examples, replace=False)
        if n_of_examples == 1:
            chat = chat_model.start_chat(
                context= input_system_prompt + "|" + input_prompt1,
            examples=[
                InputOutputTextPair(
                    input_text=random_rows.iloc[0, 1],
                    output_text=random_rows.iloc[0, 0],
                ),
                ]
                )
        else:
            chat = chat_model.start_chat(
            context= input_system_prompt + "|" + input_prompt1,
            examples=[
                InputOutputTextPair(
                    input_text=random_rows.iloc[0, 1],
                    output_text=random_rows.iloc[0, 0],
                ),
                InputOutputTextPair(
                input_text=random_rows.iloc[1, 1],
                output_text=random_rows.iloc[1, 0],
                ),
                ]
                )

    else:
        chat = chat_model.start_chat(
            context= input_system_prompt + "|" + input_prompt1)

    response = chat.send_message(input_prompt2, **parameters)
    # to send the third prompt to say: please shorter
    # response2 = chat.send_message(input_prompt3, **parameters)
    # return response2
    print(f"Response from Model: {response.text}")
    return response


def LLM_rms_evaluator(input_eval_prompt, temperature=.2):

    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,    # Token limit determines the maximum amount of text output.
        "top_p": 0.95,               # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,                 # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context = "Your task is to evaluate the radio messages."
        #examples=[
        #    InputOutputTextPair(
        #        input_text='How many moons does Mars have?',
        #        output_text='The planet Mars has two moons, Phobos and Deimos.',
       #     ),
      #  ]
    )

    response = chat.send_message(input_eval_prompt, **parameters)
    #print(f"Response from Model: {response.text}")

    return response




def gpt_generator(system_prompt, input_prompt1, input_prompt2, input_prompt3):
     # in gpt, everything must be put into 1 string.
    import openai
    openai.api_key = api_key_gpt
    
    
    assistent_reaction1 = "OK, ik begrijp je. Ik schrijf een radiobericht van ongeveer 55 woorden en maximaal 65 woorden waarin ik irrelevante informatie weg laat en mij focus op één essentieel onderdeel van het nieuwsbericht. Ik begin mijn radiobericht met Het Radiobericht:"
    
    # response1 is only used for v1 version of gpt4 generated messages
    response1 = openai.ChatCompletion.create(
                model = "gpt-4", 
                #model = "gpt-3.5-turbo", 
            messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content": input_prompt1},
            {"role": "assistant", "content": assistent_reaction1},
            {"role":"user", "content": input_prompt2}
            ]
            ,
            max_tokens = 500,
            temperature = 0.8,
            n = 1,
            stop = None
            )
    resp_1 = response1.choices[0].message.content
    print(resp_1)
    gen_rm = remove_text_before_hetradiobericht(resp_1)


    # This part is added for v2 gpt4
    user_prompt3 = input_prompt1 + "1\n" + assistent_reaction1 + " " + input_prompt2 + "2\n" + resp_1 + " " + input_prompt3 + "\n"
    # #print(user_prompt3)
    response3 = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo", 
            messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content": user_prompt3}
            ]
            ,
            max_tokens = 500,
            temperature = 0.8,
            n = 1,
            stop = None
            )
    #print(response3.choices[0].message.content)
    

    
    return gen_rm


    
    #output = response3.choices[0].message.content
    ret_output = remove_text_before_colon(resp_1)
    return ret_output
    #generated_outputs = generate_radio_mes(prompt_news_art)
    
    #return print("This is the generated output", generated_outputs)

def remove_text_before_colon(text):
    if 'Het Radiobericht:' in text:               # I check whether )space is before the dash, since it could be that it merely connects words.
                                    # by doing this, those dashes are not impacted
        text = text.split('Het Radiobericht: ', 1)[1].strip()  # I remove everything standing before the dash.
    return text


def gpt_evaluator(input):
    import openai
    openai.api_key = api_key_gpt
    time.sleep(1)


    # Since relevantie prompt does not work perfectly (it does not always understand it needs to continue giving scores after Score A: Score B: Score C: (then D, E etc.), I need to change this)
    pattern = r"(Score C: )"
    changed_input = re.sub(pattern, r"\g<1>                 Score D:                 Score E:                 Score F:                 Score G:                 Score H:", input)
    #print("does it work?", changed_input)
    #return print("see what happens")
    response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", 
            messages=[
            
            {"role":"user", "content": changed_input}
            ]
            ,
            max_tokens = 100,
            temperature = 0.4,  # variance must def. not be temp 1 since then always the same score is given.
            n = 1,
            stop = None
            )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
    #return "train_test"





def claude_generator(input_prompt1, input_prompt2, input_prompt3):
    time.sleep(5)
     # in gpt, everything must be put into 1 string.
    #import openai
    my_api = api_key_1
    user_prompt1 = "\n\nHuman: " + input_prompt1 + "\n\nAssistant:"
    user_prompt2 = "\n\nHuman: " + input_prompt2 + "\n\nAssistant:"
    user_prompt3 = "\n\nHuman: " + input_prompt3 + "\n\nAssistant:"
    #final_user_prompt = user_prompt1 + user_prompt2 + user_prompt3
    #print(final_user_prompt)
    
    #c = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
    max_tokens_to_sample = 500
    c = anthropic.Client(api_key = my_api)
    # resp1 = c.completion( prompt=user_prompt1,
    #     model="claude-v1",
    #     max_tokens_to_sample = max_tokens_to_sample,
    # )
    # print(type(resp1))
    # print()
    # print(resp1['completion'].strip())
    # completed_resp1 = resp1['completion'].strip()
    # print("Does this give a response?")
    
    completed_resp1 = "OK, ik begrijp je. Ik schrijf een radiobericht van ongeveer 55 woorden en maximaal 65 woorden waarin ik irrelevante informatie weg laat en mij focus op één essentieel onderdeel van het nieuwsbericht. Ik begin mijn radiobericht met Het Radiobericht:"

    resp2 = c.completion( prompt=user_prompt1 + completed_resp1 + user_prompt2,
        model="claude-v1",
        max_tokens_to_sample = max_tokens_to_sample,
    )
    # print(resp2['completion'].strip())
    # completed_resp2 = resp2['completion'].strip()
    # print("look for me", completed_resp2)
    # resp3 = c.completion( prompt=user_prompt1 + completed_resp1 + user_prompt2 + completed_resp2 + user_prompt3,
    #     model="claude-v1",
    #     max_tokens_to_sample = max_tokens_to_sample,
    # )
    # print("where am I", resp3['completion'].strip())
    # gen_rm = remove_text_before_enter(resp3['completion'].strip())

    #print(resp2['completion'].strip())
    gen_rm = remove_text_before_hetradiobericht(resp2['completion'].strip())



    return gen_rm





def remove_text_before_enter(text):
    if '\n\n' in text:               # I check whether )space is before the dash, since it could be that it merely connects words.
                                    # by doing this, those dashes are not impacted
        text = text.split('\n\n', 1)[1].strip()  # I remove everything standing before the dash.
    return text

def remove_text_before_hetradiobericht(text):
    keyword = 'Het Radiobericht:'
    if keyword in text:               # I check whether )space is before the dash, since it could be that it merely connects words.
                                    # by doing this, those dashes are not impacted
        text = text.split(keyword, 1)[1].strip()  # I remove everything standing before the dash.
    return text


def claude_evaluator(input):
     # in gpt, everything must be put into 1 string.
    #import openai
    #print("this is the input", input)
    my_api = api_key_1
    user_prompt1 = "\n\nHuman: " + input + "\n\nAssistant:"
    max_tokens_to_sample = 500
    c = anthropic.Client(api_key = my_api)
    resp1 = c.completion( prompt=user_prompt1,
        model="claude-v1",
        max_tokens_to_sample = max_tokens_to_sample
    )
    #print(type(resp1))
    #print()
    print(resp1['completion'].strip())
    completed_resp1 = resp1['completion'].strip()
    
    return completed_resp1