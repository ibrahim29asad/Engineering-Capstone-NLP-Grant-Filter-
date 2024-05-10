#Imports
import numpy as np
import matplotlib.pyplot as plt
import requests
import mysql.connector
from bs4 import BeautifulSoup
from keybert import KeyBERT
import os
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from nltk.corpus import wordnet
from pathlib import Path
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np
import joblib

#Function to extract useful text from web scraped page
def extract_text(content, name):
    
    blacklist_words = [
        'ucalgary',
        'institute',
        'academic',
        'faculty',
        'calgary',
        'student',
        'university',
        'graduate', 'students', 'admission', 'grants', 'apply', 'scholarships', 'alberta', 'diploma', 'postdoctoral', 'assistant', 
        'bsc', 'intern', 'professor', 'contact', 'expertise', 'phd', 'research', 'researcher', 'examinations', 'exam', 'examination', 
        'department', 'msc', 'subject', 'scholar', 'courses', 'course', 'citizen', 'citizens', 'biography', 'profile', 'lab',
        'campus', 'alumni', 'doctoral', 'alma', 'degree', 'careers'
    ]
    
    cleanText = ""
    spaced = name.split(" ")
    #Parse content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    for data in soup(['style', 'script', 'header', 'footer', 'head', 'foot', '[document]', 'meta']):
        data.decompose()
        
    cleanText = ' '.join(soup.stripped_strings)
    cleanText = cleanText.lower()
            
    for item in spaced:
        if(item == ' '):
            continue
        cleanText = cleanText.replace(item, '')
        
    for item in blacklist_words:
        cleanText = cleanText.replace(item, '')

    cleanText.replace('\n', '').replace('\r', '')
    return cleanText.strip()

def start_extraction_researchers(profile, email):
    current_folder_path = str(Path(__file__).parent)
    
    env_path = os.path.join(current_folder_path, '.env')
    load_dotenv(env_path)

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
    
    id = ""
    
    insert_check = 0
    try:
        cursor.execute("INSERT INTO researcher_profiles_urls (url, email) VALUES (%s, %s)", (profile, email))
        id = cursor.lastrowid
        db.commit()
        insert_check = 1
    except mysql.connector.IntegrityError:
        db.rollback()
        cursor.execute("SELECT id FROM researcher_profiles_urls WHERE email=%s", (email,))
        items = cursor.fetchall()
        id = items[0][0]
        insert_check = 0

    url = profile

    #Create list for irrelevant keywords

    words = url.split('/')
    names = words[-1].split('-')
    formattedstring = ""  
    for name in names:
        if len(name) > 1:
            formattedstring += " " + name
    irrel_names = formattedstring

    try:
        #For every URL, get the webpage and then save it
        res = requests.get(url, headers=headers)
        
        if res.status_code == 200:
            html_page = res.content

            #For every url, run the extract_text function, save the output, extract the keywords from the saved output, and then save the keywords
            output = extract_text(html_page, irrel_names)
            extracted_keywords = kw_model.extract_keywords(output, keyphrase_ngram_range=(1, 1), nr_candidates=40, top_n=10)

            fileName = os.path.join(current_folder_path + "/Researcher_Profiles", str(id) + " " + irrel_names + ".txt")
            file = open(fileName, "w")
            
            writing = email + "\n"
            for items in extracted_keywords:
                writing += items[0] + "\n"

            writing = writing[:-1]
            file.write(writing)
            file.close()
            
            #This section deals with loading the saved SVM model, TFIDF vectorizer, and the list of funding opportunities:
            svm_model = joblib.load(current_folder_path + '/Saved_Files/saved_model') #this contains data for the trained SVM model
            tfidf = joblib.load(current_folder_path + '/Saved_Files/saved_vectorizer') #this contains data for the TFIDF vectorizer
            all_fo = joblib.load(current_folder_path + '/Saved_Files/saved_list') #this contains the list of FOs from the training input

            
            #The line below should be changed depending on how the researcher profile is intended to be put into the program
            profile = open(current_folder_path + '/Researcher_Profiles/' + str(id) + " " + irrel_names + ".txt", 'r') #this opens the .txt file for the researcher profile.

            input_string = ''

            lines = profile.readlines()

            for line in lines[1:]:  # [1:] skips the first line, which is the email address of the researcher
              clean_line = line.rstrip('\n')  # rstrip('\n') removes the newline character at the end of each line
              input_string += " " + clean_line  #concatenates each line to the input_string string

            profile.close()

            #Vectorizing Test Input
            #Insert test input here:
            test_input = input_string
            test_input_vec = tfidf.transform([test_input])  #vectorize test input
            
            #Prediction:
            pred = svm_model.predict(test_input_vec)

            #Decision Function array:
            prob = svm_model.decision_function(test_input_vec)
            
            #Retrieve confidence values from the array from highest to lowest. 

            relevant_FO_indices = np.argsort(prob).flatten()[::-1]  #shows INDICES of decision function values in DESCENDING order

            #This section deals with outputting the relevant FO links for the researcher profile:
            relevant_links = [] #array for the relevant FO links
            researcher_keywords = test_input
            threshold = 0 #this is an adjustable value
            
            cv = CountVectorizer()
            
            researcher_vec = cv.fit_transform([researcher_keywords]) #vectorize researcher keywords
            #each fo_keyword set is vectorized inside the for-loop below

            for i in relevant_FO_indices:
                if len(relevant_links) == 20:
                    break

                #all_fo[i] takes the ith FO in the FO list, 
                #split() tokenizes the string with space as its delimiter,
                #[0] takes the first item on the list created by split(), which should give the relevant link.
                tokens = all_fo[i].split()
                link = tokens[0]
                fo_keywords = ' '.join(tokens[1:])
                
                fo_keywords_vec = cv.transform([fo_keywords]) #vectorize fo_keywords
                cosine_score = cosine_similarity(researcher_vec, fo_keywords_vec)
                
                if cosine_score > threshold:
                    relevant_links.append(link)    
                else:
                    break #get out of loop once the similarity score reaches zero within the list
                    # it is unlikely that there will be relevant links below this point. 

            sender = "ifarmtest2024@gmail.com"
            recipient = "ifarmtest2024@gmail.com"

            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = sender
            smtp_password = "rnqt nerv uqiw gklb" #this is the app password, not the actual password.

            #Creating the email:
            subject = "IFARM Test"

            body = irrel_names + " (" + email + ") \n" + " (" + url + ") \n\n" + "Relevant Links for You: \n"

            if len(relevant_links) != 0:
                for i in relevant_links:
                    body = body + i + "\n"
            else:
                body = body + "Sorry, there are no relevant funding opportunities for you at the moment. Please check again later."

            message = MIMEMultipart()
            message["From"] = sender
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(smtp_username, smtp_password)
                    server.sendmail(sender, recipient, message.as_string())
            except Exception as e:
                print(f"An error occurred: {e}")
            
        else:
            print("Did not get status 200")
            
            #Remove the entry from the database
            if insert_check == 1:
                cursor.execute("DELETE FROM researcher_profiles_urls WHERE id = %s", (id,))
                db.commit()
            else:
                return
            
    except Exception as error:
        print("An error occurred:", error)
        #Remove the entry from the database
        if insert_check == 1:
            cursor.execute("DELETE FROM researcher_profiles_urls WHERE id = %s", (id,))
            db.commit()
        else:
            return