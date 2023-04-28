from transformers import pipeline
import pandas as pd
import requests
import regex as re
import os
from symspellpy import SymSpell
import pkg_resources
from bs4 import BeautifulSoup
import random



def get_url(lccn, year):
    # Example url:
    url = f'https://chroniclingamerica.loc.gov/lccn/{lccn}/issues/{year}'
    # url = 'https://chroniclingamerica.loc.gov/lccn/sn86072192/issues/1897/'
    lccn_label = lccn.strip() 

    session = requests.Session()
    response = session.get(url).text
    # print(response)

    # Parse out issue dates from the response using regex
    pattern = r'<a href="/lccn/'+ lccn.strip() + '/' + str(year) +'-.*?>'
    matches = re.findall(pattern, response)
    
    # Return a dictionary indexed by lccn and year
    return {'lccn': lccn, 'year': year, 'matches': matches}


def get_word_rate(text, dictionary): # Function to get % of words in text that appear in a dictionary
  num_words = 0
  for word in text.split():
    if word.lower() in dictionary.keys():
      num_words += 1

  return num_words / len(text.split())

def chunk_text(text, chunk_size):
  chunks = []
  words = text.split()
  i = 0
  while i + chunk_size < len(words):
    chunks.append(' '.join(words[i: i + chunk_size]))
    i += chunk_size
  chunks.append(' '.join(words[i:]))
  return chunks

def save_matches_to_file(lccn, year, matches, chunk_number):
  # Helper function to save matches to file
  directory = f'/n/holyscratch01/kozinsky_lab/Kehang/panic/urls/{lccn.strip()}/'
  print(f'{directory}{year}.txt')
  if not os.path.exists(directory):
    os.makedirs(directory)
  with open(f'{directory}/{year}.txt', 'w') as outfile:
    outfile.writelines(matches)
    outfile.write('\n')
    outfile.writelines(chunk_number)

def get_text(lccn, year):
    # Fetch the URLs of all issues in the given year
    url_data = get_url(lccn, year)
    issue_urls = url_data['matches']
    head = 'https://chroniclingamerica.loc.gov/'
    tail = 'ocr/'
    text = ''
    score = 0
    chunk_number = 0
    old_url = head
    # Loop through all issue URLs and extract the text
    sample_size = min(10, len(issue_urls))
    random_urls = random.sample(issue_urls, sample_size)

    for issue_url in random_urls:
        # Extract the URL from the issues_url variable
        url = issue_url.strip('<a href="').strip('">')

        # Combine the URL with the head variable to form the full URL
        full_url = head + url
        response = requests.get(full_url)
        html_content = response.text
        print(full_url)
        # Use regular expression to find all matches
        pattern = r'<a href="/lccn/'+ lccn.strip() + '/' + str(year) +'-\d{2}-\d{2}/ed-1/seq-\d+/">'
        text_matches = re.findall(pattern, html_content)
        
        ## randomly pick up 2 ocrs
        sample_size2 = min(2, len(text_matches))
        random_selection = random.sample(text_matches, sample_size2)
        
        for text_url in random_selection:
            t_url = text_url.strip('<a href="').strip('">')
            ocr_url = head+ t_url + tail
            print(ocr_url)
            if (ocr_url == old_url):
                continue
            else:
                response = requests.get(ocr_url)
                ocr_content = response.text

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(ocr_content, 'html.parser')

                # Extract the text content of the desired HTML element(s)
                for elem in soup.find_all('div'):
                    if elem.find('p') is not None:
                        text = elem.find('p').get_text()
                        chunks = chunk_text(text, chunk_size)
                        for chunk in chunks:
                            rate = get_word_rate(chunk, eng_dictionary)
                            if (rate > WORD_RATE_THRESHOLD):
                                chunk_number += 1 
                                if chunk_number >  max_chunk:
                                    break
                                # score += sentiment_analysis(chunk)[0]['score']
                                data =sentiment_analysis(chunk)
                                print(data)
                        
                                if data[0]['label'] == 'NEGATIVE':
                                   score += -1 * data[0]['score']
                                elif data[0]['label'] == 'POSITIVE':
                                   score += data[0]['score']
                        if chunk_number >  max_chunk:
                            break
                        print('current score', score, 'current chunk number', chunk_number)
                        old_url = ocr_url
                        text = ''

                    if chunk_number >  max_chunk:
                        break

            if chunk_number >  max_chunk:
                break

    return str(score), str(chunk_number)


def main():
    df = pd.read_csv('/n/home09/zkh/Panic/files/modified_part_1.csv', encoding='latin-1')
    df.columns = [c.strip() for c in df.columns]
    df['First Issue Date'] = pd.to_datetime(df['First Issue Date'])
    df['Last Issue Date'] = pd.to_datetime(df['Last Issue Date'])
    df['First Issue Year'] = df['First Issue Date'].dt.year
    df['Last Issue Year'] = df['Last Issue Date'].dt.year
    df_filtered = df[(df['First Issue Year'] < 1940) & (df['Last Issue Year'] > 1920)]


    
    for index, row in df_filtered.iterrows():
        lccn = row['LCCN']
        first_year = int(row['First Issue Year'])
        last_year = int(row['Last Issue Year'])
        for year in range(first_year, last_year + 1):
            if int(year) >= 1920 and int(year) <= 1940:
                texts_score, chunk_number = get_text(lccn, year)
                # if chunk_number > 0:
                    # score = texts_score / chunk_number
                save_matches_to_file(lccn, year, texts_score, chunk_number)
            else:
                continue



if __name__ == "__main__":
    symspell = SymSpell()
    dict_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt") # Get file path for dictionary
    symspell.load_dictionary(dict_path, 0, 1) # Load in dictionary
    eng_dictionary = symspell.words # Get keyed list of english words
    
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")
    
    chunk_size = 100
    WORD_RATE_THRESHOLD = .6 # Set this to whateve
    max_chunk = 500

    main()
