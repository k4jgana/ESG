
def get_valid_orgz():
    orgz=[]
    with open('valid_comps.txt', 'r') as file:
        for line in file:
            orgz.append(line.strip())
    return orgz



def get_valids(orgz,df):
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

