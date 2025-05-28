import tkinter as tk
from tkinter import ttk,messagebox,scrolledtext,filedialog
import spacy
from utils import export_to_csv,replace_entities,regex_entity_match
import os

try:
    nlp=spacy.load('zh_core_web_sm')
except:
    import spacy.cli
    spacy.cli.download('zh_core_web_sm')
    nlp=spacy.load('zh_core_web_sm')

TARGET_LABELS=['LOC','DATE','GPE','MONEY','PHONE','EMAIL','ID','BANK','CREDIT_CARD','ADDRESS','IP','URL']

def extract_entities(text):
    ents=[]
    regex_ents=regex_entity_match(text)
    ents.extend(regex_ents)

    doc=nlp(text)
    for ent in doc.ents:
        if ent.label_ in TARGET_LABELS:
            ents.append((ent.label_,ent.text,ent.start_char))

    seen=set()
    unique_ents=[]
    for label,text_ent,start in sorted(ents,key=lambda x:x[2]):
        key=(start,len(text_ent))
        if key not in seen:
            seen.add(key)
            unique_ents.append((label,text_ent,start))
    return unique_ents

class PIIExtractorApp:
    def __init__(self,root):
        root.title('本地個資提取器 (spaCy NER)')
        root.geometry('1200x600')
        self.setup_ui(root)

    def setup_ui(self,root):
        ttk.Label(root,text='請貼上或輸入文本：').pack(anchor='w',padx=10,pady=(10,0))
        self.txt_input=scrolledtext.ScrolledText(root,height=8)
        self.txt_input.pack(fill='x',padx=10,pady=5)

        btn_extract=ttk.Button(root,text='開始提取',command=self.run_extraction)
        btn_extract.pack(pady=5)

        frm_output=tk.Frame(root)
        frm_output.pack(fill='both',expand=True,padx=10,pady=10)

        frm_left=tk.Frame(frm_output)
        frm_left.pack(side='left',fill='both',expand=True,padx=(0,5))

        ttk.Label(frm_left,text='模式1：提取個資').pack(anchor='w')
        self.txt_mode1=scrolledtext.ScrolledText(frm_left)
        self.txt_mode1.pack(fill='both',expand=True)

        frm_right=tk.Frame(frm_output)
        frm_right.pack(side='left',fill='both',expand=True,padx=(5,0))

        ttk.Label(frm_right,text='模式2：替換原文個資(標籤格式)').pack(anchor='w')
        self.txt_mode2=scrolledtext.ScrolledText(frm_right)
        self.txt_mode2.pack(fill='both',expand=True)

    def run_extraction(self):
        text=self.txt_input.get('1.0','end').strip()
        if not text:
            messagebox.showwarning('警告','請輸入文本')
            return
        entities=extract_entities(text)
        if not entities:
            messagebox.showinfo('提示','未偵測到個資')
            return

        lines=[]
        count_dict={}
        for label,text_entity,_ in entities:
            count_dict[label]=count_dict.get(label,0)+1
            lines.append(f'{label}{count_dict[label]} | {text_entity}')
        output1='\n'.join(lines)
        self.txt_mode1.delete('1.0','end')
        self.txt_mode1.insert('1.0',output1)

        replaced=replace_entities(text,entities)
        self.txt_mode2.delete('1.0','end')
        self.txt_mode2.insert('1.0',replaced)

if __name__=='__main__':
    os.makedirs('output',exist_ok=True)
    root=tk.Tk()
    app=PIIExtractorApp(root)
    root.mainloop()
