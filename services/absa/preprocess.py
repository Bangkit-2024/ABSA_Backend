import pandas as pd
import numpy as np
import re
import emoji
import unicodedata
from services.services import translate_services
import multiprocessing
from utils.STATICVAR import PROCESS_TIMEOUT


class PreprocessData:
    def __init__(self,timeout=PROCESS_TIMEOUT):
        self.timeout = PROCESS_TIMEOUT
        # Load the CSV file into a DataFrame
        df_kamusalay = pd.read_csv('services/absa/model/new_kamusalay.csv', encoding='latin1')
        self.word_map = dict(zip(df_kamusalay.iloc[0], df_kamusalay.iloc[1]))

        # Load the abusive words from abusive.csv into a set
        df_abusive = pd.read_csv('services/absa/model/abusive.csv')
        self.abusive_words = set(df_abusive['ABUSIVE'])


        # Custom stemming dictionary
        self.custom_stem_dict = {
            'pelayanan': 'pelayanan',
            'pelayanannya': 'pelayanan',
            'pelayan': 'pelayanan',
            'layanan': 'pelayanan'
        }

    def _worker_function(input_str, queue):
        try:
            result = translate_services(input_str)
            queue.put(result)
        except Exception as e:
            queue.put(input_str)

    def translate_with_timeout(self, input_str, timeout):
        queue = multiprocessing.Queue()  # Create a queue for communication
        
        # Create a process for the function
        process = multiprocessing.Process(target=self._worker_function, args=(input_str, queue))
        process.start()
        
        # Wait for the process to complete with a timeout
        process.join(timeout)
        
        # If the process is still running after the timeout, terminate it
        if process.is_alive():
            process.terminate()
            process.join()
            return input_str  # Return the original input string if the process timed out
        
        # Check if the queue has a result
        if not queue.empty():
            result = queue.get()
            return result
        else:
            return input_str  # Return the original input string if no result is found in the queue


    def case_folding(self, text):
        return text.lower()

    def remove_non_ascii(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')

    def remove_punctuation(self, text):
        return re.sub(r'[^\w\s]', ' ', text)

    def remove_repeated_characters(self, text):
        return re.sub(r'\b(\w*?)([^grnlmo])\2+(\w*)\b', r'\1\2\3', text)

    def fix_typos(self, text):
        words = text.split()
        normalized_words = [self.word_map.get(word, word) for word in words]
        return ' '.join(normalized_words)

    def remove_abusive_words(self, text):
        words = text.split()
        clean_words = [word for word in words if word.lower() not in self.abusive_words]
        return ' '.join(clean_words)

    def remove_whitespace(self, text):
        return re.sub(r'\s+', ' ', text).strip()

    def emojize(self, text):
        return emoji.demojize(text)

    def remove_stopwords(self, tokens):
        return [word for word in tokens if word not in self.stopwords]

    def stemming(self, text):
        words = text.split()
        stemmed_words = [self.custom_stem_dict.get(word, self.stemmer.stem(word)) for word in words]
        return ' '.join(stemmed_words)

    def remove_numbers(self, text):
        return re.sub(r'\d+', '', text)

    def preprocess_text(self, old_text):
        text = self.translate_with_timeout(old_text,self.timeout)
        text = self.remove_non_ascii(text)
        text = self.case_folding(text)
        text = self.remove_punctuation(text)
        text = self.remove_repeated_characters(text)
        text = self.fix_typos(text)
        text = self.remove_abusive_words(text)
        text = self.remove_whitespace(text)
        text = self.emojize(text)
        text = self.remove_numbers(text)
        
        return text