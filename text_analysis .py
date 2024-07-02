#!/usr/bin/env python
# coding: utf-8

# In[89]:


import os
import nltk
import pyphen
import re
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# In[90]:


stop_words = set()

# Directory containing stop word files
stopword_dir = 'StopWords'

# Read all files in the directory
for filename in os.listdir(stopword_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(stop_word_dir, filename), 'r', encoding='latin-1') as f:  # Specify encoding
            stop_words.update(f.read().splitlines())

print("Stop Words:", stop_words)


# In[91]:


# Directory containing the Master Dictionary files
masterdict_dir = 'MasterDictionary'

# Initialize sets for positive and negative words
positive_words = set()
negative_words = set()

# Read positive words from file
positive_file = os.path.join(masterdict_dir, 'positive-words.txt')
with open(positive_file, 'r', encoding='latin-1') as f:  # Use latin-1 encoding
    positive_words.update(word.strip() for word in f if word.strip() not in stop_words)

# Read negative words from file
negative_file = os.path.join(masterdict_dir, 'negative-words.txt')
with open(negative_file, 'r', encoding='latin-1') as f:  # Use latin-1 encoding
    negative_words.update(word.strip() for word in f if word.strip() not in stop_words)

print("Positive Words:", positive_words)
print("Negative Words:", negative_words)


# In[92]:


pip install pyphen


# In[93]:


# Initialize Pyphen dictionary
dic = pyphen.Pyphen(lang='en')

def count_syllables(word):
    """Returns the number of syllables in a word."""
    word = word.lower()
    syllable_count = 0
    vowels = "aeiou"
    current_word = word
    if word.endswith("es") or word.endswith("ed"):
        current_word = word[:-2]

    for char in current_word:
        if char in vowels:
            syllable_count += 1
    return max(1, syllable_count)

# Load stop words from nltk
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Personal pronouns regex pattern
personal_pronouns = re.compile(r'\b(I|we|my|ours|us)\b', re.I)

# Read positive and negative words from the master dictionary
with open('MasterDictionary/positive-words.txt', 'r', encoding='ISO-8859-1') as f:
    positive_words = set(f.read().split())

with open('MasterDictionary/negative-words.txt', 'r', encoding='ISO-8859-1') as f:
    negative_words = set(f.read().split())

# Initialize list to store readability results
readability_results = []

# Iterate over each file in the 'articles' folder
for filename in sorted(os.listdir('articles')):
    if filename.endswith('.txt'):
        file_path = os.path.join('articles', filename)
        
        # Read the text from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Tokenize the text into sentences and words
        sentences = sent_tokenize(text)
        words = word_tokenize(text)

        # Remove stop words and punctuations from the word list
        words_cleaned = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]

        # Sentiment Analysis
        positive_score = sum(1 for word in words_cleaned if word in positive_words)
        negative_score = sum(1 for word in words_cleaned if word in negative_words)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / (len(words_cleaned) + 0.000001)

        # Calculate Average Sentence Length
        average_sentence_length = len(words_cleaned) / len(sentences)

        # Count the number of complex words (words with more than 2 syllables)
        complex_words = [word for word in words_cleaned if count_syllables(word) > 2]
        complex_word_count = len(complex_words)

        # Calculate Percentage of Complex Words
        percentage_complex_words = (complex_word_count / len(words_cleaned)) * 100

        # Calculate Fog Index
        fog_index = 0.4 * (average_sentence_length + percentage_complex_words)

        # Calculate Average Number of Words Per Sentence
        avg_words_per_sentence = len(words_cleaned) / len(sentences)

        # Calculate Total Word Count
        word_count = len(words_cleaned)

        # Calculate Syllable Count Per Word
        syllable_count_per_word = [count_syllables(word) for word in words_cleaned]
        avg_syllable_count_per_word = sum(syllable_count_per_word) / len(syllable_count_per_word)

        # Count Personal Pronouns
        personal_pronoun_count = len(personal_pronouns.findall(text))

        # Calculate Average Word Length
        total_characters = sum(len(word) for word in words_cleaned)
        avg_word_length = total_characters / len(words_cleaned)

        # Store the readability results
        readability_results.append({
            'URL_ID': filename,
            'Positive Score': positive_score,
            'Negative Score': negative_score,
            'Polarity Score': polarity_score,
            'Subjectivity Score': subjectivity_score,
            'Average Sentence Length': average_sentence_length,
            'Percentage of Complex Words': percentage_complex_words,
            'Fog Index': fog_index,
            'Average Number of Words Per Sentence': avg_words_per_sentence,
            'Complex Word Count': complex_word_count,
            'Word Count': word_count,
            'Average Syllables Per Word': avg_syllable_count_per_word,
            'Personal Pronouns': personal_pronoun_count,
            'Average Word Length': avg_word_length
        })

# Convert the results to a DataFrame
df = pd.DataFrame(readability_results)

# Save the results to an Excel file
output_file = 'output_file.xlsx'
df.to_excel(output_file, index=False)

print(f'Readability results have been saved to {output_file}')


# In[ ]:





# In[ ]:




