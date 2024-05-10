from sklearn import svm

from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import joblib
import os
from pathlib import Path

def start_training():
    current_folder_path = str(Path(__file__).parent)
    #This section takes in individual FO .txt files and joins them into one .txt file called Training_Input.txt
    #Training_Input.txt is then parsed to ensure that only the extracted keywords are put into the SVM model
    all_fo = [] #this array will contain the input training data

    folder_path = os.path.join(current_folder_path, 'Funding_Opportunities')

    files = os.listdir(folder_path)

    output_file = open(os.path.join(current_folder_path, 'Training_Input.txt'), 'w', encoding="utf-8")

    for file in files:
        if file.endswith('.txt'):
            input_file = open(os.path.join(current_folder_path + '/Funding_Opportunities', file), 'r', encoding="utf-8") #open the .txt file
            read_input_file = input_file.readline() + '\n'
            output_file.write(read_input_file)
            input_file.close()

    output_file.close()

    train_input = open(os.path.join(current_folder_path, 'Training_Input.txt'), 'r', encoding="utf-8")
            
    input_lines = train_input.readlines()

    #This for loop creates an array which stores a list of keywords for funding opportunities in each index.
    for line in input_lines:
        words = line.split()
        rejoined_line = ' '.join(words[1:])
        clean_line = rejoined_line.rstrip('\n')  # rstrip('\n') removes the newline character at the end of each line
        all_fo.append(clean_line)

    train_input.close()

    # Vectorize the keyword sets with binary representation
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(all_fo)
    #print(X.shape)

    #Labels:

    y = []

    for i in range(len(all_fo)):
      y.append(i)

    #This takes care of the labels for each feature in the training set. 

    #SVM Model
    #Build SVM model
    svm_model = svm.SVC(kernel = 'linear', probability = True)
    svm_model.fit(X,y)

    #This section deals with deleting the pre-existing SVM model, vectorizer, and list and then saving them again.

    if os.path.exists(current_folder_path + '/Saved_Files/saved_model'):
        os.remove(current_folder_path + '/Saved_Files/saved_model')
    joblib.dump(svm_model, current_folder_path + '/Saved_Files/saved_model')

    if os.path.exists(current_folder_path + '/Saved_Files/saved_vectorizer'):
        os.remove(current_folder_path + '/Saved_Files/saved_vectorizer')
    joblib.dump(tfidf, current_folder_path + '/Saved_Files/saved_vectorizer')

    if os.path.exists(current_folder_path + '/Saved_Files/saved_list'):
        os.remove(current_folder_path + '/Saved_Files/saved_list')
    joblib.dump(input_lines, current_folder_path + '/Saved_Files/saved_list')