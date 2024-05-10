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
from datetime import datetime
import os
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from pathlib import Path
import Training_Model
from dotenv import load_dotenv

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

def start_extraction_funding(url, date):
    current_folder_path = str(Path(__file__).parent)
    
    env_path = os.path.join(current_folder_path, '.env')
    load_dotenv(env_path)

    final_directory = os.path.join(current_folder_path, r'Funding_Opportunities')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    nltk.download('stopwords')
    
    #Create a list of stopwords
    stopwords2 = stopwords.words('english')
    stopwords2.append('grant')
    stopwords2.append('grantee')
    stopwords2.append('grants')
    stopwords2.append('award')
    stopwords2.append('awards')
    stopwords2.append('apply')
    stopwords2.append('applying')
    stopwords2.append('application')
    stopwords2.append('applicant')
    stopwords2.append('applicants')
    stopwords2.append('applications')
    stopwords2.append('proposal')
    stopwords2.append('proposals')
    stopwords2.append('deadline')
    stopwords2.append('fund')
    stopwords2.append('funds')
    stopwords2.append('funding')

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

    dateAndTime = datetime.today().strftime('%Y-%m-%d')    

    id = ""
    try:
        #Code that deletes all text files of outdated url links
        cursor.execute("SELECT id FROM funding_opportunity_urls WHERE closeDate < %s", (dateAndTime,))
        outdated_ids = cursor.fetchall()
        for ID in outdated_ids:
            fileName = os.path.join(current_folder_path + "/Funding_Opportunities", str(ID[0]) + ".txt")
            if os.path.exists(fileName):
                os.remove(fileName)
                print(ID, "Removed\n")

        try:
            cursor.execute("INSERT INTO archived_links (url, closeDate, reason) SELECT url,closeDate,'Archived' FROM funding_opportunity_urls WHERE closeDate < %s", (dateAndTime,))
            db.commit()
            
        except Exception as error:
            print("URL already in archived database:",error)
                
        cursor.execute("DELETE FROM funding_opportunity_urls WHERE closeDate < %s", (dateAndTime,))
        db.commit()
        
        cursor.execute("INSERT INTO funding_opportunity_urls (url, closeDate) VALUES (%s, %s)", (url, date))
        id = cursor.lastrowid
        db.commit()
    except mysql.connector.IntegrityError:
        db.rollback()
        cursor.execute("SELECT id FROM funding_opportunity_urls WHERE url=%s", (url,))
        items = cursor.fetchall()
        id = items[0][0]

    #For every URL, get the webpage and then save it
    try:
        res = requests.get(url, headers=headers)
        
        #If we get the webpage...
        if res.status_code == 200:
            content_type = res.headers.get('content-type')
            
            if 'application/pdf' in content_type:
                pdf_page = res.content
                temp = ''
                with BytesIO(pdf_page) as data:
                    read_pdf = PdfReader(data)
                    for page in range(len(read_pdf.pages)):
                        temp = temp + read_pdf.pages[page].extract_text()
                pdfoutput = temp
                extracted_keywords = kw_model.extract_keywords(pdfoutput, keyphrase_ngram_range=(1, 1), stop_words = stopwords2, nr_candidates=40, top_n=15) #For every url, run the extract_text function, save the output, extract the keywords from the saved output, and then save the keywords
            
            #Get contents now, then use keywords array
            elif 'text/html' in content_type:
                html_page = res.content
                htmloutput = extract_text_self(html_page)
                extracted_keywords = kw_model.extract_keywords(htmloutput, keyphrase_ngram_range=(1, 1), stop_words = stopwords2, nr_candidates=40, top_n=15) #For every url, run the extract_text function, save the output, extract the keywords from the saved output, and then save the keywords
            
            fileName = os.path.join(current_folder_path + "/Funding_Opportunities", str(id) + ".txt")
            file = open(fileName, "w")
            writing = url + " "
            for items in extracted_keywords:
                writing += items[0] + " "
            writing = writing[:-1]
            file.write(writing)
            file.close()
            
            Training_Model.start_training()
        
        #If we cannot access the webpage...
        else:
            print("Did not get status 200");
            
            #Remove the entry from the database
            cursor.execute("DELETE FROM funding_opportunity_urls WHERE id = %s", (id,))
            db.commit()
            
            #Output the link that did not work to the archived_links table
            try:
                cursor.execute("INSERT INTO archived_links (url, reason) VALUES (%s, %s)", (url, "Did not get status 200"))
                db.commit()
                
            except Exception as error:
                print("URL already in archived database:",error)    
    #If we run into an error when trying to access the website (SSL error) or when trying to train the model...
    except Exception as error:
        print("Error encountered:",error)
        
        #Remove the entry from the database
        cursor.execute("DELETE FROM funding_opportunity_urls WHERE id = %s", (id,))
        db.commit()
        
        #Output the link that did not work to the archived_links table
        try:
            cursor.execute("INSERT INTO archived_links (url, reason) VALUES (%s, %s)", (url, "SSL Error"))
            db.commit()
            
        except Exception as error:
            print("URL already in archived database:",error)