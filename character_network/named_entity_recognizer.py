import spacy
from nltk.tokenize import sent_tokenize
from ast import literal_eval
import os
import pandas as pd
from utils import load_subtitles_dataset

class NamedEntityRecognizer:
    def __init__(self):
        self.nlp_model = self.load_model()
    
    def load_model(self):
        nlp = spacy.load("en_core_web_sm")
        return nlp
    
    def get_ners_inference(self, script):
        script_sentences = sent_tokenize(script)
        ner_output = []
        
        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            ners = set()
            for entity in doc.ents:
                if entity.label_ == 'PERSON':
                    full_name = entity.text
                    first_name = entity.text.split(" ")[0].strip()
                    ners.add(first_name)
            ner_output.append(ners)
            
        return ner_output
    
    def get_ners(self, dataset_path, save_path=None):
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df['ners'] = df['ners'].apply(lambda x: literal_eval(x) if isinstance(x, str) else x)
            return df
        
        # Load the dataset
        df = load_subtitles_dataset(dataset_path)
        
        # Corrected assignment syntax
        df['ners'] = df['script'].apply(self.get_ners_inference)
        
        # Save the DataFrame if a save path is provided
        if save_path is not None:
            df.to_csv(save_path, index=False)
        
        return df
