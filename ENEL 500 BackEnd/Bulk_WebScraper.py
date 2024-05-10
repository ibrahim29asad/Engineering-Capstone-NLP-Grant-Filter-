#Imports
import numpy as np
import matplotlib.pyplot as plt
import requests
import mysql.connector
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from keybert import KeyBERT
from io import BytesIO
from PyPDF2 import PdfReader
import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from pathlib import Path
from dotenv import load_dotenv

current_folder_path = str(Path(__file__).parent)

env_path = os.path.join(current_folder_path, '.env')
load_dotenv(env_path)

final_directory = os.path.join(current_folder_path, r'Funding_Opportunities')
if not os.path.exists(final_directory):
    os.makedirs(final_directory)
		
#Create a list of stopwords
stopwords = stopwords.words('english')
stopwords.append('grant')
stopwords.append('grantee')
stopwords.append('grants')
stopwords.append('award')
stopwords.append('awards')
stopwords.append('apply')
stopwords.append('applying')
stopwords.append('application')
stopwords.append('applicant')
stopwords.append('applicants')
stopwords.append('applications')
stopwords.append('proposal')
stopwords.append('proposals')
stopwords.append('deadline')
stopwords.append('fund')
stopwords.append('funds')
stopwords.append('funding')

#Initialize keybert
kw_model = KeyBERT()


#Set user agent
#Allows access to websites prevent web-scraping
headers = {'User-Agent': 
           'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}


db = mysql.connector.connect(
    host = os.getenv('DATABASE_HOST'),
    user = os.getenv('DATABASE_USER'),
    password = os.getenv('DATABASE_PASSWORD'),
    database = os.getenv('DATABASE')
)

cursor = db.cursor()

#Function to extract useful text from web scraped page
def extract_text_self(content):
    cleanText = ''
    
    #Parse content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    for data in soup(['style', 'script', 'header', 'footer', 'head', 'foot', '[document]', 'meta']):
        data.decompose()
        
    cleanText = ' '.join(soup.stripped_strings)
    
    cleanText.replace('\n', '').replace('\r', '')
    return cleanText.strip()

html_page = {}
pdf_page = {}
pdfoutput = {}
htmloutput = {}
extracted_keywords = {}

cursor.execute("SELECT url FROM funding_opportunity_urls")

urls = cursor.fetchall()

cursor.execute("SELECT id FROM funding_opportunity_urls")

all_ids = cursor.fetchall()

#For every URL, get the webpage and then save it
for (url, ids) in zip(urls, all_ids):
    try:
        res = requests.get(url[0], headers=headers)
        
        #If we get the webpage...
        if res.status_code == 200:
            content_type = res.headers.get('content-type')
            
            if 'application/pdf' in content_type:
                pdf_page[url[0]] = res.content
                temp = ''
                with BytesIO(pdf_page[url[0]]) as data:
                    read_pdf = PdfReader(data)
                    for page in range(len(read_pdf.pages)):
                        temp = temp + read_pdf.pages[page].extract_text()
                pdfoutput[url[0]] = temp
                extracted_keywords[url[0]] = kw_model.extract_keywords(pdfoutput[url[0]], keyphrase_ngram_range=(1, 1), stop_words = stopwords, nr_candidates=40, top_n=15) #For every url, run the extract_text function, save the output, extract the keywords from the saved output, and then save the keywords
            
            #Get contents now, then use keywords array
            elif 'text/html' in content_type:
                html_page[url[0]] = res.content
                htmloutput[url[0]] = extract_text_self(html_page[url[0]])
                extracted_keywords[url[0]] = kw_model.extract_keywords(htmloutput[url[0]], keyphrase_ngram_range=(1, 1), stop_words = stopwords, nr_candidates=40, top_n=15) #For every url, run the extract_text function, save the output, extract the keywords from the saved output, and then save the keywords       

            fileName = os.path.join(current_folder_path + "/Funding_Opportunities", str(ids[0]) + ".txt")
            file = open(fileName, "w", encoding="utf-8")              
            writing = url[0] + " "
            for items in extracted_keywords[url[0]]:
                writing += items[0] + " "    
            writing = writing[:-1]
            file.write(writing)
            file.close()
            
        #If we cannot access the webpage...
        else:
            print("Did not get status 200");
            
            #Remove the entry from the database
            cursor.execute("DELETE FROM funding_opportunity_urls WHERE id = %s", (ids[0],))
            db.commit()
            
            #Output the link that did not work to the archived_links table
            try:
                cursor.execute("INSERT INTO archived_links (url, reason) VALUES (%s, %s)", (url[0], "Did not get status 200"))
                db.commit()
                
            except Exception as error:
                print("URL already in archived database:",error)    

    #If we run into an error when trying to access the website (SSL error) or when trying to train the model...
    except Exception as error:
        print("Error encountered:",error)
        
        #Remove the entry from teh database
        cursor.execute("DELETE FROM funding_opportunity_urls WHERE id = %s", (ids[0],))
        db.commit()
        
        #Output the link that did not work to the archived_links table
        try:
            cursor.execute("INSERT INTO archived_links (url, reason) VALUES (%s, %s)", (url[0], "SSL Error"))
            db.commit()
            
        except Exception as error:
            print("URL already in archived database:",error)