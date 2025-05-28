import csv
import os
import re
REGEX_PATTERNS = {
    'PHONE': r'\b09[0-9]{8}\b',

    'EMAIL': r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b',
    
    'ID': r'\b[A-Z][12][0-9]{8}\b',
    
    'BANK': r'\b\d{3}-[0-9]{7,14}\b',
    
    'IP': r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
    
    'URL': r'\b(?:https?://|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?\b',
    
    'ADDRESS': r'(?:路|街|道)(?P<detail>(?:[一二三四五六七八九十0-9]{1,3}段)?(?:\d+巷)?(?:\d+弄)?\d{1,5}號(?:之\d{1,3})?(?:\d{1,3}樓|[一二三四五六七八九十]{1,3}樓)?(?:\d+室)?)',

    'CREDIT_CARD': r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|6(?:011|5[0-9]{2})[0-9]{12}|(?:2131|1800|35\d{3})\d{11})\b'
}
def export_to_csv(entities, filename):
    os.makedirs(os.path.dirname(filename),exist_ok=True)
    with open(filename,mode='w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f)
        writer.writerow(['類別','內容'])
        for label,text in entities:
            writer.writerow([label,text])

def replace_entities(text, entities):
    count_dict={}
    replaced_text=text
    entities=sorted(entities,key=lambda x:x[2],reverse=True)
    for label,entity_text,start in entities:
        count_dict[label]=count_dict.get(label,0)+1
        placeholder=f'<{label}{count_dict[label]}>'
        replaced_text=replaced_text[:start]+placeholder+replaced_text[start+len(entity_text):]
    return replaced_text

def regex_entity_match(text):
    ents=[]
    for label,pattern in REGEX_PATTERNS.items():
        for match in re.finditer(pattern,text):
            ents.append((label,match.group(),match.start()))
    return ents