import pandas as pd
from services import scrapperService, bertService, neo4jService, dataService, openaiService
import json

# Read the JSON configuration file
with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Extract keys, model, and prompt
keys = list(config_data['openAI']['keys'].values())
model = config_data['openAI']['model']
prompt = config_data['prompt']

df=pd.read_csv("data.csv")


# new_df=scrapperService.scrape_to_date(df)
# new_df.head()
# new_df = new_df[new_df['Title'] != "ESG Today: Week in Review"]
# new_df.to_csv("new_df.csv",index=False)
new_df = pd.read_csv("new_df.csv")
texts=dataService.truncate_text_in_dataframe(new_df,500)
tenses=openaiService.label_data(texts,keys,prompt,model)
new_df["Tense"]=tenses
new_df.to_csv("new_df.csv",index=False)
new_df=bertService.get_orgz(new_df)
new_df.to_csv("new_df.csv",index=False)
vdf=dataService.get_valids(new_df)
if neo4jService.test_connection():
    neo4jService.insert_to_neo4j(vdf)
    print("proccess done")

