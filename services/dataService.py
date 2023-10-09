import tiktoken


def truncate_text_in_dataframe(df, max_tokens):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    def split_into_sentences(text):
        sentences = text.split('. ')
        return sentences

    def truncate_sentences(sentences, max_tokens):
        truncated_sentences = []
        tokens_so_far = 0

        for sentence in sentences:
            tokens = len(tokenizer.encode(" " + sentence))
            if tokens_so_far + tokens <= max_tokens:
                truncated_sentences.append(sentence)
                tokens_so_far += tokens
            else:
                break

        return truncated_sentences

    shortened_texts = []

    for _, row in df.iterrows():
        if row['Text'] is None:
            continue

        sentences = split_into_sentences(row['Text'])
        truncated_sentences = truncate_sentences(sentences, max_tokens)

        if truncated_sentences:
            truncated_text = ". ".join(truncated_sentences) + "."
            shortened_texts.append(truncated_text)

    return shortened_texts



def get_valid_orgz():
    orgz=[]
    with open('C:\\Users\\itquarks\\Desktop\\fax\BetterV\\ESG\\valid_comps.txt', 'r') as file:
        for line in file:
            orgz.append(line.strip())
    return orgz



def get_valids(df):
    orgz=get_valid_orgz()
    # Your list of strings
# Initialize an empty dictionary to store the official names and their aliases
    aliases = {}
    # Iterate through the list and split each element at "->"
    for item in orgz:
        if "->" in item:
            parts = item.split(" -> ")
            alias = parts[0].strip()
            official_name = parts[1].strip()

            # Check if the alias already exists in the dictionary
            if alias in aliases:
                # If it does, append the official name to the existing list of official names
                aliases[alias].append(official_name)
            else:
                # If it doesn't, create a new entry with the alias and official name as a list
                aliases[alias] = [official_name]
        else:
            aliases[item] = [item]

    dff=df.explode("Organizations")
    vdf=dff[dff["Organizations"].isin(list(aliases.keys()))]
    return vdf

