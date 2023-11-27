#########################################################
#### Written By: SATYAKI DE                          ####
#### Written On: 24-Nov-2023                         ####
#### Modified On 26-Nov-2023                         ####
####                                                 ####
#### Objective: This is the main calling             ####
#### python script that will invoke the              ####
#### RAG class, which will get the contexts with     ####
#### reference inclduing source files, line numbes   ####
#### and source texts. This will help customer to    ####
#### validate the source against the OpenAI response ####
#### to understand & control the data bias & other   ####
#### potential critical issues.                      ####
####                                                 ####
#########################################################

from openai import OpenAI
import faiss
import clsL as log
import numpy as np
import os
import re
import pickle
from gensim.models import KeyedVectors

import clsTemplate as ct

from clsConfigClient import clsConfigClient as cf

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

os.environ["TOKENIZERS_PARALLELISM"] = "false"

vectorDBFileName = cf.conf['VECTORDB_FILE_NM']
vectorDBPath = cf.conf['VECTORDB_PATH']

indexFile = str(vectorDBPath) + str(vectorDBFileName) + '.index'
print('File: ', str(indexFile))

index = faiss.read_index(indexFile)

# Initialize your data dictionary
# Load the data dictionary
data = {}
vectorDBPath = cf.conf['VECTORDB_PATH']
modelFileName = cf.conf['CACHE_FILE']

dataCache = vectorDBPath + modelFileName

modelPath = cf.conf['MODEL_PATH']

with open(dataCache, 'rb') as f:
    data = pickle.load(f)

# Configure the default for all requests:
client = OpenAI(
    api_key = cf.conf['OPEN_AI_KEY'],
    # default is 60s
    timeout=20.0,
)

###############################################
###    End of Global Section                ###
###############################################

class clsRAGOpenAI:
    def __init__(self):
        self.basePath = cf.conf['DATA_PATH']
        self.fileName = cf.conf['FILE_NAME']
        self.Ind = cf.conf['DEBUG_IND']
        self.subdir = str(cf.conf['OUT_DIR'])
        self.base_url = cf.conf['BASE_URL']
        self.outputPath = cf.conf['OUTPUT_PATH']
        self.vectorDBPath = cf.conf['VECTORDB_PATH']
        self.openAIKey = cf.conf['OPEN_AI_KEY']
        self.temp = cf.conf['TEMP_VAL']
        self.modelName = cf.conf['MODEL_NAME']
        self.maxToken = cf.conf['MAX_TOKEN']
        self.maxCount = cf.conf['MAX_CNT']
        # Load the Glove model
        self.model = KeyedVectors.load_word2vec_format(modelPath + 'glove.6B.100d.w2vformat.txt')

    def getTopKContexts(self, queryVector, k):
        try:
            distances, indices = index.search(queryVector, k)
            resDict = [(data[i]['file_name'], data[i]['line_number'], data[i]['text']) for i in indices[0]]
            return resDict
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return x

    def generateOpenaiPrompt(self, queryVector, k):
        contexts = self.getTopKContexts(queryVector, k)
        template = ct.templateVal_1
        prompt = template
        for file_name, line_number, text in contexts:
            prompt += f"Document: {file_name}\n Line Number: {line_number} \n Content: {text}\n\n"
        return prompt

    def ragAnswerWithHaystackAndGPT3(self, queryVector, k, question):
        modelName = self.modelName
        maxToken = self.maxToken
        temp = self.temp

        # Assuming getTopKContexts is a method that returns the top K contexts
        contexts = self.getTopKContexts(queryVector, k)
        messages = []

        # Add contexts as system messages
        for file_name, line_number, text in contexts:
            messages.append({"role": "system", "content": f"Document: {file_name} \nLine Number: {line_number} \nContent: {text}"})

        prompt = self.generateOpenaiPrompt(queryVector, k)
        prompt = prompt + "Question: " + str(question) + ". \n Answer based on the above documents."

        # Add user question
        messages.append({"role": "user", "content": prompt})

        # Create chat completion
        completion = client.chat.completions.create(
        model=modelName,
        messages=messages,
        temperature = temp,
        max_tokens = maxToken
        )

        # Assuming the last message in the response is the answer
        last_response = completion.choices[0].message.content
        source_refernces = ['FileName: ' + str(context[0]) + ' - Line Numbers: ' + str(context[1]) + ' - Source Text (Reference): ' + str(context[2]) for context in contexts]

        return last_response, source_refernces

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

    def getData(self, strVal):
        try:
            maxCount = self.maxCount
            print('*' * 240)
            print('Loading Your Data & Index for Retrieval:')
            print('*' * 240)

            print('Response from New Docs: ')
            print()

            qVector = self.text2Vector(strVal)
            qVector = qVector.reshape(-1)
            top_k = maxCount

            answer, source_refernces = self.ragAnswerWithHaystackAndGPT3(np.array([qVector]), top_k, strVal)

            print('*' * 240)
            print()
            print(' ' * 110 + 'GPT3 Answer::')
            print()
            print('*' * 240)
            print(answer)
            print()
            print('*' * 240)
            print()
            print(' ' * 110 + 'Source Reference::')
            print()
            print('*' * 240)
            print()
            for extractedText in source_refernces:
                print(str(extractedText))
                print()

            print('*' * 240)
            print('End Of Use RAG to Generate Answers:')
            print('*' * 240)

            return answer, source_refernces
        except Exception as e:
            x = str(e)
            print('Error: ', x)
            answer = x
            source_refernces = "Not Found!"

            return answer, source_refernces
