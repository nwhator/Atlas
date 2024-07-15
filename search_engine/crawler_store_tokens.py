import pickle
import os
from bs4 import BeautifulSoup
import requests

def save_tokenized_text(tokeninzed_text, filename):
    with open(filename, 'wb') as f:
        pickle.dump(tokeninzed_text, f)
    
if not os.path.exists('tokenized_text_pickle.pkl'):
    websites = [
        'http://localhost:5000/peter',
        'http://localhost:5000/lois',
        'http://localhost:5000/chris',
        'http://localhost:5000/meg',
        'http://localhost:5000/stewie'
    ]

    text_content = []
    for website in websites:
        response = requests.get(website)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content.append(soup.get_text())
        else:
            text_content.append('')
        
    stop_words = ['the', 'is', 'and', 'to', 'Hi', 'my', 'name', 'a', 'in', 'that', 'for', 'it', 'Click', 'here', 'go']

    tokenized_text = []
    for content in text_content:
        tokens = content.lower().split()
        tokenized_text.append([token for token in tokens if token not in stop_words])
        
    save_tokenized_text(tokenized_text, 'tokenized_text_pickle.pkl')
