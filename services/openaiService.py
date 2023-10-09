import openai,time,random

def label_text(text,prompt,model_name):
    prompt.replace("<<TEXT>>",text)
    response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content":prompt}
                ],
                temperature=0,
                max_tokens=512,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )
    return response['choices'][0]['message']['content']


def label_data(texts, list_openai_keys, prompt, model_name):
    print(f"labeling started on {len(texts)} texts")
    i = 0
    tenses = []
    for text in texts:
        i += 1
        time.sleep(random.uniform(1, 2))
        if i % 50 == 0:
            print(i)
            time.sleep(random.uniform(12, 15))
        try:
            tense = label_text(text, prompt, model_name)
            print(tense)
            tenses.append(tense)  # Move this line inside the try block
        except:
            if openai.api_key == list_openai_keys[0]:
                openai.api_key = list_openai_keys[1]
            else:
                openai.api_key = list_openai_keys[0]
            print(f"CHANGING KEY AT {i}")
    return tenses  # Ensure that the return statement is outside the loop
