 #!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd


# In[8]:


input_df = pd.read_excel('Input.xlsx')


# In[9]:


print(input_df.head())


# In[10]:


import requests
from bs4 import BeautifulSoup
import os



# In[11]:


def extract_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the main content section with the class 'td-post-content'
        main_content = soup.find("div", {"class": "td-post-content"})
        
        if main_content:
            article_content = main_content.get_text(strip=True)
            return article_content
        else:
            print(f'Main content section not found on {url}')
            return None
    except Exception as e:
        print(f'Error extracting article from {url}: {e}')
        return None



# In[12]:


# Ensure the 'articles' directory exists
os.makedirs('articles', exist_ok=True)

for index, row in input_df.iterrows():
    url = row['URL']
    url_id = row['URL_ID']

    print(f'Processing URL_ID: {url_id}, URL: {url}')
    article_content = extract_article(url)

    if article_content:
        with open(f'articles/{url_id}.txt', 'w', encoding='utf-8') as f:
            f.write(article_content)
        print(f'Successfully extracted: {url_id}')
    else:
        print(f'Failed to extract content for URL_ID {url_id}')


# In[ ]:




