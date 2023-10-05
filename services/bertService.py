from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
import pandas as pd

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

def get_orgz(df):
    titles=df['Titles'].tolist()
    ners=get_ners(titles)
    orgz=process_orgz(ners,titles)
    df["Organizations"]=orgz
    return df


def get_ners(titles):
    i=0
    ners=[]
    for title in titles:
        try:
            ners.append(nlp(title))
        except:
            print(f"Exception:{i}")
        i+=1
            


def process_orgz(ners,titles):
    start_ends=[]
    for sent in ners:
        start_ends_sent=[]
        for els in sent:
            if "ORG" in els['entity']:
                start_ends_sent.append([els['start'],els['end'],els['entity']])
        start_ends.append(start_ends_sent)
    
    orgz = []
    
    for sent, title in zip(start_ends, titles):
        orgz_within = [] 
        organizations = []  
        
        for el in sent:
            if el[2] == "B-ORG":
                if organizations:  
                    orgz_within.append(''.join(organizations))
                    organizations = []  
                organizations.append(title[el[0]:el[1]])  
            elif el[2] == "I-ORG":
                organizations.append(title[el[0]:el[1]])  
        if organizations:  
            orgz_within.append(''.join(organizations))
    
        if not orgz_within:  
            orgz_within.append('NOT FOUND')
        orgz.append(orgz_within)  
    return orgz
