from vertexai.preview.language_models import ChatModel, InputOutputTextPair


def science_tutoring( input_prompt1, input_prompt2, input_prompt3, temperature=.2):

    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,    # Token limit determines the maximum amount of text output.
        "top_p": 0.95,               # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,                 # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context= input_prompt1
        #examples=[
        #    InputOutputTextPair(
        #        input_text='How many moons does Mars have?',
        #        output_text='The planet Mars has two moons, Phobos and Deimos.',
       #     ),
      #  ]
    )

    response = chat.send_message(input_prompt2, **parameters)
    print(f"Response from Model: {response.text}")

    # I want to continue in the same chat to ask input_prompt3, but I am not sure whether it allows me to do that 
    # since now it uses start.chat, and I need function continue.chat.

    return response