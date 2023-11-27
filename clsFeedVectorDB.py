#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 24-Nov-2023                         ####
#### Modified On 26-Nov-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### faiss frameowrk to contextulioze the docs       ####
#### inside the vector DB with source file name to   ####
#### validate the answer from Gen AI using Globe.6B  ####
#### embedding models.                               ####
####                                                 ####
#########################################################

import numpy as np
import faiss
import os
import pickle
from gensim.models import KeyedVectors
import gensim.downloader as api

from clsConfigClient import clsConfigClient as cf
import clsL as log

from datetime import datetime, timedelta

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

###############################################
###           Global Section                ###
###############################################

Ind = cf.conf['DEBUG_IND']

#Initiating Logging Instances
clog = log.clsL()

var = datetime.now().strftime(".%H.%M.%S")

modelPath = cf.conf['MODEL_PATH']

###############################################
###    End of Global Section                ###
###############################################

class clsFeedVectorDB:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.modelFileName = cf.conf['CACHE_FILE']
        self.vectorDBPath = cf.conf['VECTORDB_PATH']
        self.vectorDBFileName = cf.conf['VECTORDB_FILE_NM']
        # Load the Glove model
        self.model = KeyedVectors.load_word2vec_format(modelPath + 'glove.6B.100d.w2vformat.txt')

    # Sample function to convert text to a vector
    def text2Vector(self, text):
        # Encode the text using the tokenizer
        words = [word for word in text.lower().split() if word in self.model]

        # If no words in the model, return a zero vector
        if not words:
            return np.zeros(self.model.vector_size)

        # Compute the average of the word vectors
        vector = np.mean([self.model[word] for word in words], axis=0)
        return vector.reshape(1, -1)

    def genData(self):
        try:
            basePath = self.basePath
            modelFileName = self.modelFileName
            vectorDBPath = self.vectorDBPath
            vectorDBFileName = self.vectorDBFileName

            # Create a FAISS index
            dimension = int(cf.conf['NO_OF_MODEL_DIM'])  # Assuming 100-dimensional vectors 
            index = faiss.IndexFlatL2(dimension)

            print('*' * 240)
            print('Vector Index Your Data for Retrieval:')
            print('*' * 240)

            FullVectorDBname = vectorDBPath + vectorDBFileName
            indexFile = str(vectorDBPath) + str(vectorDBFileName) + '.index'

            print('File: ', str(indexFile))

            data = {}
            # List all files in the specified directory
            files = os.listdir(basePath)

            # Filter out files that are not text files
            text_files = [file for file in files if file.endswith('.txt')]

            # Read each text file
            for file in text_files:
                file_path = os.path.join(basePath, file)
                print('*' * 240)
                print('Processing File:')
                print(str(file_path))
                try:
                    # Attempt to open with utf-8 encoding
                    with open(file_path, 'r', encoding='utf-8') as file:
                        for line_number, line in enumerate(file, start=1):
                            # Assume each line is a separate document
                            vector = self.text2Vector(line)
                            vector = vector.reshape(-1)
                            index_id = index.ntotal

                            index.add(np.array([vector]))  # Adding the vector to the index
                            data[index_id] = {'text': line, 'line_number': line_number, 'file_name': file_path}  # Storing the line and file name
                except UnicodeDecodeError:
                    # If utf-8 fails, try a different encoding
                    try:
                        with open(file_path, 'r', encoding='ISO-8859-1') as file:
                            for line_number, line in enumerate(file, start=1):
                                # Assume each line is a separate document
                                vector = self.text2Vector(line)
                                vector = vector.reshape(-1)
                                index_id = index.ntotal
                                index.add(np.array([vector]))  # Adding the vector to the index
                                data[index_id] = {'text': line, 'line_number': line_number, 'file_name': file_path}  # Storing the line and file name
                    except Exception as e:
                        print(f"Could not read file {file}: {e}")
                        continue

                print('*' * 240)

            # Save the data dictionary using pickle
            dataCache = vectorDBPath + modelFileName
            with open(dataCache, 'wb') as f:
                pickle.dump(data, f)

            # Save the index and data for later use
            faiss.write_index(index, indexFile)

            print('*' * 240)

            return 0

        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return 1
