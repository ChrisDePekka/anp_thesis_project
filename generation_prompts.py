import re

def generate_prompts_clavie(zero_cot, instructions, mock, reit, right, info, name, pos):
    # the base prompt now isnt really fixed unfortunately, since the baseprompt would be:
    # base_prompt = "Schrijf een radiobericht van het volgende nieuwsbericht: "

    base_prompt = "Nu geef ik jou een nieuwsbericht en jij analyseert het en schrijft er vervolgens een radio bericht van."

    if zero_cot:
        prompt1 = base_prompt
        prompt2 = "Antwoord: denk stap-voor-stap na"
    if instructions:
        system_prompt = "Jij bent een AI journalist die expert is in het schrijven van radio berichten. Jouw taak is om van het nieuwsartikel een bericht te schrijven dat bestemd is voor een radio-uitzending. Jij bent creatief. Jij gebruikt liever woorden die niet in het nieuwsartikel voorkomen. Gebruik begrijpelijke taal dat door een breed publiek kan worden begrepen. "
        
        
        user_prompt = " Een radio bericht is goed als het de essentie van het nieuwsbericht bezit. Minder belangrijke nieuwsfeiten moet je niet benoemen. Ieder nieuwsfeit mag maar 1 keer benoemd worden. Als je het nieuwsbericht analyseert, neem dan mee dat de mening van mensen belangrijk is. Benoem niet de voornaam als de persoon niet het hoofdonderwerp is. Het radio bericht moet kort en bondig zijn, en geschreven in 1 paragraaf. "

        if name:
            #name_sys_prompt = ""
            #pattern = r"(bent(?:\W+\w+)*)(een)"
            pattern = r"(bent)(\s+een)"
            #name_sys_prompt = re.sub(pattern, r"\1 Christian,  \2", system_prompt)
            system_prompt = re.sub(pattern, r"\g<1>, Christian,\g<2>", system_prompt)
            #print("nammeee prompt", name_sys_prompt)
            #print("system promptss:", system_prompt)
            #print('huh')
        if reit:
            # stap-voor-stap
            
            reit_prompt = " Denk eraan, jij bent de beste AI journalist en je gebruikt jouw expertise om het best mogelijke radio bericht te schrijven."

            pattern = r"(het(?:\W+\w+)*)(\s+en)"
            new_sentence = re.sub(pattern, r"\1, stap-voor-stap,\2", prompt1)
            #print(new_sentence)
            #print("system_prompt",  system_prompt)
            prompt1 = system_prompt + reit_prompt + user_prompt + new_sentence
        else:
            prompt1 = system_prompt + user_prompt + prompt1


    if mock:
        mock_prompt =  " Begrijp je dat?"
        prompt1 = prompt1 + mock_prompt

    # loose is not expected to give good results, so I skipped it for now;

    if right:
        prompt2 = prompt2 + " zodat je het juiste antwoord bereikt."
    
    if info:
        # don't know how to incorporate this'
        print("missing")

    if pos:
        pos_prompt = "Fijn! Dan beginnen wij :)  . Voor het volgende nieuwsbericht: "
        prompt2 = pos_prompt + prompt2
    else:
        neutral_prompt = "Voor het volgende nieuwsbericht: "
        prompt2 = neutral_prompt + prompt2

    prompt3 = "Dankjewel! Kan je het iets korter schrijven?"
    
    starting_question_prompt = "Fijn! Dan beginnen wij :)  . Voor het volgende nieuwsbericht: "
    return prompt1, prompt2, prompt3


def generate_lai_eval_prompts():
    # Voor nu doe ik simpelweg 1 prompt, maar hier kan je nog prima variaties in aanbrengen.

    lai_prompt = "Voor de taak om van nieuwsberichten radio-berichten te creeëren, geef een score aan de mate waarin de content \
        bewaard blijft met betrekking tot het nieuwsbericht op een schaal van 0 tot 100. 100 geef je als alle content \
            van het nieuwsbericht bewaard blijft, en 0 geef je als het volledige incorrect is of een andere betekenis heeft. \
                Het evaluatie format is zo: \
                Output 1: \
                Score 1: \
                Uitleg 1: \
                ———————"
    return lai_prompt