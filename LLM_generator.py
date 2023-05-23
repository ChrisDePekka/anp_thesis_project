from vertexai.preview.language_models import ChatModel, InputOutputTextPair
from data_processing import get_data
from constants import examples, csv_file, n_of_examples
import openai
from config import api_key
import asyncio
import os
import anthropic




def LLM_rm_generator(input_system_prompt, input_prompt1, input_prompt2, input_prompt3, temperature=.2):

    chat_model = ChatModel.from_pretrained("chat-bison@001")

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




def gpt_generator(system_prompt, input_prompt1, input_prompt2, input_prompt3, temperature=.2):
     # in gpt, everything must be put into 1 string.
    import openai
    #openai.api_key = "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"
    user_prompt1 = input_prompt1 + "1\n"
    user_prompt2 = input_prompt2 + "2\n"
    user_prompt3 = input_prompt3 + "\n"
    final_user_prompt = user_prompt1 + user_prompt2 + user_prompt3
    print(final_user_prompt)
    
    return "test_radio_mess"
    response = openai.ChatCompletion.create(
                model = "gpt-3.5-turbo", 
            messages=[
            {"role":"system", "content":system_prompt},
            {"role":"user", "content": final_user_prompt}
            ]
            ,
            max_tokens = 150,
            temperature = 0.8,
            n = 1,
            stop = None
            )
    return response.choices[0].message.content
    #generated_outputs = generate_radio_mes(prompt_news_art)
    
    #return print("This is the generated output", generated_outputs)

def gpt_evaluator(input):
    import openai
    openai.api_key = "x"

    # response = openai.ChatCompletion.create(
    #         model = "gpt-3.5-turbo", 
    #         messages=[
            
    #         {"role":"user", "content": input}
    #         ]
    #         ,
    #         max_tokens = 150,
    #         temperature = 0.8,
    #         n = 1,
    #         stop = None
    #         )
    #return response.choices[0].message.content
    return "train_test"





def claude_generator(system_prompt, input_prompt1, input_prompt2, input_prompt3, temperature=.2):
     # in gpt, everything must be put into 1 string.
    import openai
    my_api = api_key
    user_prompt1 = "\n\nHuman: " + input_prompt1 + "\n\nAssistant:"
    user_prompt2 = "\n\nHuman: " + input_prompt2 + "\n\nAssistant:"
    user_prompt3 = "\n\nHuman: " + input_prompt3 + "\n\nAssistant:"
    final_user_prompt = user_prompt1 + user_prompt2 + user_prompt3
    print(final_user_prompt)
    
    # c = anthropic.Client(os.environ["ANTHROPIC_API_KEY"])
    # resp = await c.acompletion(
    #     prompt=f"{anthropic.HUMAN_PROMPT} How many toes do dogs have?{anthropic.AI_PROMPT}",
    #     stop_sequences=[anthropic.HUMAN_PROMPT],
    #     model="claude-v1",
    #     max_tokens_to_sample=max_tokens_to_sample,
    # )
    # print(resp)
    # }'
    return response.choices[0].message.content
    #generated_outputs = generate_radio_mes(prompt_news_art)
    
    #return print("This is the generated output", generated_outputs)