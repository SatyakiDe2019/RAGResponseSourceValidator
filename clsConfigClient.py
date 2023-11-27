################################################
#### Written By: SATYAKI DE                 ####
#### Written On:  15-May-2020               ####
#### Modified On: 28-Jun-2023               ####
####                                        ####
#### Objective: This script is a config     ####
#### file, contains all the keys for        ####
#### personal OpenAI-based MAC-shortcuts    ####
#### enable bot.                            ####
####                                        ####
################################################

import os
import platform as pl

class clsConfigClient(object):
    Curr_Path = os.path.dirname(os.path.realpath(__file__))

    os_det = pl.system()
    if os_det == "Windows":
        sep = '\\'
    else:
        sep = '/'

    conf = {
        'APP_ID': 1,
        'ARCH_DIR': Curr_Path + sep + 'arch' + sep,
        'PROFILE_PATH': Curr_Path + sep + 'profile' + sep,
        'LOG_PATH': Curr_Path + sep + 'log' + sep,
        'DATA_PATH': Curr_Path + sep + 'data' + sep,
        'OUTPUT_PATH': Curr_Path + sep + 'output' + sep,
        'TEMP_PATH': Curr_Path + sep + 'temp' + sep,
        'IMAGE_PATH': Curr_Path + sep + 'Image' + sep,
        'SESSION_PATH': Curr_Path + sep + 'my-app' + sep + 'src' + sep + 'session' + sep,
        'OUTPUT_DIR': 'model',
        'APP_DESC_1': 'RAG-based response with source-data validation Demo!',
        'DEBUG_IND': 'Y',
        'INIT_PATH': Curr_Path,
        'FILE_NAME': 'input.json',
        'MODEL_NAME': "gpt-3.5-turbo",
        'API_KEY': "4zHX5D5eKnHPRT0XXZNGZtjQUxgRoDlvLP2eLHD7",
        'MODEL_NAME': 'gpt-3.5-turbo',
        'OPEN_AI_KEY': "sk-wVz5yI6KJKHYYUHGF93983JJHHJO6jrlxPkdjTY7Bgvv",
        'YOUTUBE_KEY': "AIzaJdhdhudYHH8KX8U-EKIo3g-lko8wKI0JU",
        'TITLE': "RAG-based response with source-data validation Demo!",
        'TEMP_VAL': 0.2,
        'PATH' : Curr_Path,
        'MAX_TOKEN' : 512,
        'MAX_CNT' : 5,
        'OUT_DIR': 'data',
        'OUTPUT_DIR': 'output',
        'MERGED_FILE': 'mergedFile.csv',
        'CLEANED_FILE': 'cleanedFile.csv',
        'CLEANED_FILE_SHORT': 'cleanedFileMod.csv',
        'SUBDIR_OUT': 'output',
        'SESSION_CACHE_FILE': 'sessionCacheCounter.csv',
        'CACHE_FILE': 'data.pkl',
        "VECTORDB_PATH": Curr_Path + sep + 'vectorDB' + sep,
        "VECTORDB_FILE_NM": "Q_A",
        "INPUT_VAL": 1000000000,
        'YEAR_RANGE': 1,
        'MODEL_PATH': Curr_Path + sep + 'NLP_Model' + sep + 'glove.6B' + sep,
        'NO_OF_MODEL_DIM': 100
    }
